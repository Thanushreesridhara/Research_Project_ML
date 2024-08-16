import torch
import hashlib
import os
from nn_classification import SimpleClassifier

# Define the number of input features and output classes
in_features = 46  
num_classes = 8   


# Ensure the secure_models directory exists
if not os.path.exists('secure_models'):
    os.makedirs('secure_models')

# Save your model
model = SimpleClassifier(in_features, num_classes)
torch.save(model.state_dict(), 'secure_models/model.pth')

# Generate checksum
def generate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

model_path = 'secure_models/model.pth'
checksum = generate_checksum(model_path)

# Print the checksum to verify it's generated correctly
print(f"Generated checksum: {checksum}")

# Save checksum to a file
with open('secure_models/model_checksum.txt', 'w') as f:
    f.write(checksum)
