import math

import torch

# distribution of 1000 random points in the domain [-10, 10]^2
maximum_value = 10
minimum_value = -10
input_tensor = (maximum_value - minimum_value) * torch.rand(1000, 2) + minimum_value

function_values = []

# value of f for each point
for i in range(1000):
    x1 = input_tensor[i][0]
    x2 = input_tensor[i][1]
    value = torch.sin(x1 + x2 / math.pi)
    function_values.append(value)

function_values = torch.tensor(function_values)
# create the pairs
pairs = torch.column_stack((input_tensor, function_values))
# print(pairs)

# save database
torch.save(pairs, "mydataset.dat")
