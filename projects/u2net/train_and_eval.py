import math
import torch
import distributed_utils as utils
import torch.nn.functional as F

def get_params_groups(model: torch.nn.Module,weight_decay = 1e-4):
    params_group = [{"params":[],"weight_decay":0},
                    {"params":[],"weight_decay":weight_decay}]
    for name ,param in model.named_parameters():
        if not param.requires_grad:
            continue
        if len(param.shape) ==1 or name.endswith(".bias"):
            params_group[0]["params"].append(param) 
        else:
            params_group[1]["params"].append(param) 

    return params_group


def create_lr_scheduler(optimizer,
                        num_step:int,
                        epochs:int,
                        warmup = True,
                        warmup_epochs = 1,
                        warmup_factor = 1e-3,
                        end_factor = 1e-6):
    assert num_step >0 and epochs >0
    if warmup is False:
        warmup_epochs = 0

    def f(x):
        if warmup is True and x<=(warmup_epochs *num_step):
            alpha = float(x) / (warmup_epochs * num_step)
            return warmup_factor * (1 - alpha) + alpha
        else:
            current_step = (x - warmup_epochs * num_step)
            cosine_steps = (epochs - warmup_epochs) * num_step
            return ((1 + math.cos(current_step * math.pi / cosine_steps)) / 2) * (1 - end_factor) + end_factor
        
    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda = f)

def criterion(inputs, target):
    losses = [F.binary_cross_entropy_with_logits(inputs[i],target) for i in range(len(inputs))] 
    total_loss = sum(losses)
    return total_loss

def train_one_epoch(model, optimizer, data_loader, device, epoch,lr_scheduler,print_freq = 10,scaler = None):
    model.train()
    metric_logger = utils.MetricLogger(delimiter = " ")
    metric_logger.add_meter("lr",utils.SmoothedValue(window_size = 1,fmt='{value:.6f}'))
    header = 'Epoch: [{}]'.format(epoch)

    for image, target in metric_logger.log_every(data_loader,print_freq, header):
        image, target = image.to(device), target.to(device)
        with torch.cuda.amp.autocast(enabled = scaler is not None):
            output = model(image)
            loss = criterion(output,target)
        
        optimizer.zero_grad()
        if scaler is not None:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        lr_scheduler.step()
        lr = optimizer.param_groups[0]["lr"]
        metric_logger.update(loss = loss.item(), lr = lr)

    return metric_logger.meters["loss"].global_avg, lr



def evaluate(model,data_loader,device):
    model.eval()
    mae_metric = utils.MeanAbsoluteError()
    f1_metric = utils.F1Score()
    metric_logger = utils.MetricLogger(delimiter = " ") 
    header = 'Test:'
    with torch.no_grad():
        for images, targets in metric_logger.log_every(data_loader,100, ):
            images,targets = images.to(device),targets.to(device)
            output = model(images)
            mae_metric.update(output,targets)
            f1_metric.update(output,targets)

        mae_metric.gather_from_all_processes()
        f1_metric.reduce_from_all_processes()
    return mae_metric, f1_metric