import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE


dfs = []
for i in range(0,3):
    filename = f"Dataset/part-00000-363d1ba3-8ab5-4f96-bc25-4d5862db7cb9-c000.csv"
    if i >=10 :
        filename = f"Dataset/part-00000-363d1ba3-8ab5-4f96-bc25-4d5862db7cb9-c000.csv"
    df_test = pd.read_csv("Dataset/part-00005-363d1ba3-8ab5-4f96-bc25-4d5862db7cb9-c000.csv")
    df = pd.read_csv(filename)
    dfs.append(df)

labels_to_remove = ['DictionaryBruteForce', 'BrowserHijacking', 'XSS', 'Uploading_Attack', 'SqlInjection', 'CommandInjection', 'Backdoor_Malware']

def change_label(df):
    df.label.replace(['DDoS-ICMP_Flood','DDoS-UDP_Flood','DDoS-TCP_Flood','DDoS-PSHACK_Flood','DDoS-SYN_Flood','DDoS-RSTFINFlood','DDoS-SynonymousIP_Flood','DDoS-ICMP_Fragmentation','DDoS-UDP_Fragmentation','DDoS-ACK_Fragmentation','DDoS-HTTP_Flood','DDoS-SlowLoris'],'DDos',inplace=True)
    df.label.replace(['DoS-UDP_Flood','DoS-TCP_Flood','DoS-SYN_Flood','DoS-HTTP_Flood'],'DoS',inplace=True)      
    df.label.replace(['Recon-HostDiscovery','Recon-OSScan','Recon-PortScan','Recon-PingSweep','VulnerabilityScan'],'Recon',inplace=True)
    df.label.replace(['MITM-ArpSpoofing','DNS_Spoofing'],'Spoofing',inplace=True)
    df.label.replace(['DictionaryBruteForce'],'BruteForce',inplace=True)
    df.label.replace(['BrowserHijacking','XSS','Uploading_Attack','SqlInjection','CommandInjection','Backdoor_Malware'],'Web-based',inplace=True)
    df.label.replace(['Mirai-greeth_flood','Mirai-udpplain','Mirai-greip_flood'],'Mirai',inplace=True)
    df.label.replace(['BenignTraffic'],'BENIGN',inplace=True)
change_label(df)

df['label'] =df['label'].replace({'BENIGN': 0, 'DDos': 1,'DoS':2,'Mirai':3,'Spoofing':4,'Recon':5,'Web-based':6,'BruteForce':7})

df_sampled = df.sample(n=22528,random_state=45)

df_remaining = df.drop(df_sampled.index)

# Save the remaining data to a CSV file
df_remaining.to_csv('remaining_data.csv', index=False)


X=df_sampled.iloc[:,:-1].values
y=df_sampled.iloc[:,-1].values

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

print(np.bincount(y))

smote = SMOTE(random_state=42, k_neighbors=2)
X_resampled, y_resampled = smote.fit_resample(X, y)

df_resampled = pd.DataFrame(X_resampled, columns=df_sampled.columns[:-1])
df_resampled['label'] = y_resampled

df_resampled.to_csv('resampled_data.csv', index=False)


X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=45)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

train_input = torch.tensor(X_TRAIN, dtype = torch.float).to(device)
test_input = torch.tensor(X_TEST, dtype = torch.float).to(device)
train_label = torch.tensor(Y_TRAIN, dtype = torch.int64).to(device)
test_label =torch.tensor(Y_TEST, dtype = torch.int64).to(device)


class SimpleClassifier(nn.Module):
    
    def __init__(self, in_features, out_features):
        super().__init__()
        self.layer_1 = nn.Linear(in_features, 128)
        self.layer_2 = nn.Linear(128, 64)
        self.layer_3 = nn.Linear(64, out_features)
        
    def forward(self, x):
        x = self.layer_3(self.layer_2(self.layer_1(x)))
        return x

in_features = X_TRAIN.shape[1]
print(in_features)
num_classes = len(set(y))
print(num_classes)

model = SimpleClassifier(in_features, num_classes).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 40
for epoch in range(num_epochs):
    model.train()
    outputs = model(train_input)
    loss = criterion(outputs, train_label)
    _, predicted_labels = torch.max(outputs,1)
    correct_predictions = (predicted_labels == train_label).sum().item()
    total_samples = len(train_label)
    acc = correct_predictions / total_samples
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {acc:.4f}' )
        
label_mapping = {
    0: 'BENIGN',
    1: 'DDos',
    2: 'DoS',
    3: 'Mirai',
    4: 'Spoofing',
    5: 'Recon',
    6: 'Web-based',
    7: 'BruteForce'
    # Add all your categories here
}

# Function to convert numerical prediction to categorical label
def get_categorical_label(numerical_label):
    return label_mapping[numerical_label]

# Set the model to evaluation mode
model.eval()

# Make predictions on the test data
with torch.no_grad():
    outputs = model(test_input)
    _, predicted_labels = torch.max(outputs, 1)

# Calculate the accuracy
correct_predictions = (predicted_labels == test_label).sum().item()
total_samples = len(test_label)
acc = correct_predictions / total_samples

print(f'Test Accuracy: {acc:.4f}')

# Define the number of examples to display
num_examples = 5

# Ensure num_examples does not exceed the size of the test set
num_examples = min(num_examples, len(test_input))

# Loop through the specified number of examples
for example_index in range(num_examples):
    example_input = test_input[example_index]
    example_output = model(example_input.unsqueeze(0))
    _, example_prediction = torch.max(example_output, 1)

    # Convert numerical prediction and correct label to categorical labels
    example_prediction_categorical = get_categorical_label(example_prediction.item())
    correct_label_categorical = get_categorical_label(test_label[example_index].item())

    print(f'Example {example_index + 1} prediction: {example_prediction_categorical}')
    print(f'Example {example_index + 1} correct label: {correct_label_categorical}')
    print()
