from flask import Flask, request, render_template, redirect, url_for, flash, abort
import pandas as pd
import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import os
from nn_classification import SimpleClassifier
import plotly.graph_objs as go
import plotly.express as px
from sklearn.metrics import confusion_matrix, classification_report
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# # Security headers
# Talisman(app)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour"]
)
limiter.init_app(app)

# Authentication setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

in_features = 46
num_classes = 8

# Generate checksum
def generate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Verify checksum
def verify_checksum(file_path, checksum_path):
    if not os.path.exists(file_path) or not os.path.exists(checksum_path):
        logging.error("Model file or checksum file not found!")
        raise FileNotFoundError("Model file or checksum file not found!")
    
    with open(checksum_path, 'r') as f:
        stored_checksum = f.read().strip()
    
    current_checksum = generate_checksum(file_path)
    
    if stored_checksum != current_checksum:
        logging.error("Model file integrity check failed!")
        raise ValueError("Model file integrity check failed!")

# Load your trained model securely
model = SimpleClassifier(in_features, num_classes)
model_path = os.path.join('secure_models', 'model.pth')
checksum_path = os.path.join('secure_models', 'model_checksum.txt')

# Verify model integrity
verify_checksum(model_path, checksum_path)

# Load the state dictionary into the model
model.load_state_dict(torch.load(model_path))

# Define the label mapping
label_mapping = {
    0: 'BENIGN',
    1: 'DDos',
    2: 'DoS',
    3: 'Mirai',
    4: 'Spoofing',
    5: 'Recon',
    6: 'Web-based',
    7: 'BruteForce'
}

def get_categorical_label(numerical_label):
    return label_mapping[numerical_label]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # authentication logic
        if username == 'admin' and password == 'password':
            user = User(id=1)
            login_user(user)
            return redirect(url_for('upload_predict'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
@limiter.limit("100 per minute")
def upload_predict():
    if request.method == 'POST':
        csv_file = request.files['file']
        if not csv_file:
            return "No file"
        
        # Validate file type
        if not csv_file.filename.endswith('.csv'):
            abort(400, description="Invalid file type. Only CSV files are allowed.")
        
        # Create the uploads directory if it doesn't exist
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file_path = os.path.join('uploads', secure_filename(csv_file.filename))
        csv_file.save(file_path)

        data = pd.read_csv(file_path)
        y_true = data.iloc[:, -1].values
        # Preprocess the data
        X = data.iloc[:,:-1].values
        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)
        X = torch.tensor(X, dtype=torch.float)

        # Make predictions
        with torch.no_grad():
            outputs = model(X)
            _, predicted_labels = torch.max(outputs, 1)

        # Convert numerical predictions to categorical labels
        predicted_labels_categorical = [get_categorical_label(label.item()) for label in predicted_labels]

        # Add the predictions to the dataframe
        data['Predicted Label'] = predicted_labels_categorical

        # Generate confusion matrix
        cm = confusion_matrix(y_true, predicted_labels.numpy())
        cm_figure = go.Figure(data=go.Heatmap(
            z=cm,
            x=list(label_mapping.values()),
            y=list(label_mapping.values()),
            colorscale='Blues',
            hoverongaps=False))

        cm_figure.update_layout(
            title='Confusion Matrix',
            xaxis_nticks=len(label_mapping),
            yaxis_nticks=len(label_mapping))
        cm_div = cm_figure.to_html(full_html=False)

        # Generate distribution bar chart
        predicted_counts = pd.Series(predicted_labels.numpy()).value_counts().sort_index()
        dist_figure = px.bar(x=predicted_counts.index, y=predicted_counts.values, labels={'x': 'Labels', 'y': 'Count'}, title='Distribution of Predicted Labels')
        dist_div = dist_figure.to_html(full_html=False)

        # Display any 3 rows
        sample_data_html = data.sample(6).to_html(classes='data')

        return render_template('display.html', cm_div=cm_div, dist_div=dist_div, sample_data_html=sample_data_html)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
