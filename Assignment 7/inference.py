import math

import torch
import torch.nn.functional as F

import myModel

# we load the model

filepath = "myNet.pt"
ann = myModel.Net(2, 10, 1)

ann.load_state_dict(torch.load(filepath))
ann.eval()

# visualise the parameters for the ann (aka weights and biases)
for name, param in ann.named_parameters():
    if param.requires_grad:
        print(name, param.data)


x = float(input("Give x: "))
y = float(input("Give y: "))
input_tensor = torch.tensor([x, y])
print(ann(input_tensor).tolist())
print(torch.sin(torch.tensor(x) + torch.tensor(y)/math.pi))


