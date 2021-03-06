from __future__ import print_function
import torch
import torch.utils.data
from torch import nn, optim
from torch.nn import functional as F
from torchvision import datasets, transforms
from torchvision.utils import save_image

from classes.models_vae import VAE
from classes.training_VAE import TrainerVAE

import numpy as np

torch.manual_seed(123)

batch_size = 128
epochs = 10
log_interval = 10

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

kwargs = {'num_workers': 1, 'pin_memory': True} if torch.cuda.is_available() else {}

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data/mnist', train=True, download=True,
                   transform=transforms.ToTensor()),
    batch_size=batch_size, shuffle=True, **kwargs)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data/mnist', train=False, transform=transforms.ToTensor()),
    batch_size=batch_size, shuffle=True, **kwargs)


VAE = VAE()
vae_optimizer = optim.Adam(VAE.parameters(), lr=1e-3)
trainer_VAE = TrainerVAE(VAE, vae_optimizer, device)
trainer_VAE.train_VAE(train_loader, test_loader, epochs, log_interval, batch_size)

name = 'mnist'
torch.save(trainer_VAE.model.state_dict(), './models/VAE_' + name + '.pt')

np.save("./models/train_losses_" + name + ".npy", np.asarray(trainer_VAE.train_losses))
np.save("./models/test_losses_" + name + ".npy", np.asarray(trainer_VAE.test_losses))
