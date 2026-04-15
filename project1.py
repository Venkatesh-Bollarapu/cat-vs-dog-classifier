import sys
import torch
from torchvision.models import mobilenet_v2
from torchvision import transforms
from PIL import Image
import torch.nn as nn

# Image path
img_path = sys.argv[1]

# Transform
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
])

# Load model
model = mobilenet_v2(weights=None)
model.classifier = nn.Sequential(
    nn.Dropout(0.2),
    nn.Linear(1280, 512),
    nn.ReLU(inplace=True),
    nn.Dropout(0.5),
    nn.Linear(512, 2)
)
model.load_state_dict(torch.load("mobilenetv2_model.pth", map_location='cpu'))
model.eval()

# Load and transform image
img = Image.open(img_path).convert('RGB')
img = transform(img).unsqueeze(0)

# Predict
with torch.no_grad():
    pred = model(img).argmax(dim=1).item()

print("cat" if pred==0 else "dog")
