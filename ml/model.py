import torch.nn as nn
from torchvision import models

def get_deepfake_model():
    model = models.efficientnet_b0(weights=None)

    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, 2)  # <-- MUST BE 2

    return model
