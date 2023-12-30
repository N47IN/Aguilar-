import pandas as pd
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Define the neural network model
class MyNetwork(nn.Module):
    def __init__(self):
        super(MyNetwork, self).__init__()
        self.fc1 = nn.Linear(10, 64)  
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)  
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(32, 2)   

    def forward(self, x):
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.fc3(x)
        return x

class CustomDataset(Dataset):
    def __init__(self, input):
        self.input = pd.read_csv(input)
        outputs = self.input.iloc[2:5, 2:72].values
        inputs = self.input.iloc[7:13, 2:72].values
        sc = StandardScaler()
        x_train = sc.fit_transform(inputs)
        y_train = outputs
        self.Xtrain = torch.tensor(x_train,dtype=torch.float32)
        self.Ytrain = torch.tensor(y_train)

    def __len__(self):
        return len(self.Ytrain)

    def __getitem__(self,idx):
        return self.Xtrain[idx],self.Ytrain[idx]
# Instantiate the model

dataset = CustomDataset('output.csv')
train_size = 0.8
train_dataset, test_dataset = train_test_split(dataset, train_size=train_size, test_size=1 - train_size, random_state=42)
batch_size = 64  # Adjust as needed
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

model = MyNetwork()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
num_epochs = 100

for epoch in range(num_epochs):
    model.train()
    for inputs, targets in train_dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets.unsqueeze(1))  # Assuming a single output
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        test_loss = 0.0
        for inputs, targets in test_dataloader:
            outputs = model(inputs)
            test_loss += criterion(outputs, targets.unsqueeze(1)).item()

    average_test_loss = test_loss / len(test_dataloader)
    print(f'Epoch {epoch + 1}/{num_epochs}, Test Loss: {average_test_loss}')

model.eval()
