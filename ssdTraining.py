import torch
from torchvision import models, transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

# Transformations
transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.ToTensor(),
])

# Load dataset
dataset = ImageFolder(root='path/to/dataset', transform=transform)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

# Load SSD model pre-trained on COCO
model = models.detection.ssdlite320_mobilenet_v3_large(pretrained=True)

# Replace the classifier with a new one (number of classes)
num_classes = 256  # adjust according to your dataset
in_features = model.head.classification_head.conv[0].in_channels
model.head.classification_head = torchvision.models.detection.ssdlite.SSDClassificationHead(in_features, num_classes)

# Training
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

optimizer = torch.optim.SGD(model.parameters(), lr=0.005, momentum=0.9, weight_decay=0.0005)

for epoch in range(10):  # change number of epochs
    model.train()
    for images, targets in dataloader:
        images = [image.to(device) for image in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()
