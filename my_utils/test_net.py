import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.linear = nn.Linear(3,3)

    def forward(self,x):
        x = self.linear(x)
        return x
    
if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # x = torch.ones(1,device = "cuda:0")
    x = torch.rand((1000,3),device = device)
    y = x*2
    net = Net()
    net.to(device)
    lr = 0.01
    momentum = 0.9
    optim = torch.optim.SGD(net.parameters(),lr,momentum = momentum)
    loss_func = torch.nn.MSELoss()
    
    for epoch in range(1000):
        pred = net(x)
        optim.zero_grad()
        loss = loss_func(pred,y)
        loss.backward()
        optim.step()
        print(loss.item())
    
    with torch.no_grad():
        x = torch.ones((1,3),device = device)
        pred = net(x)
        print(pred)
        
