import datetime
import time
from my_dataset import DUTSDataset
import transforms as T
import os
import torch
from torch.utils import data
from typing import List, Union
from model import U2Net
from train_and_eval import create_lr_scheduler, get_params_groups, train_one_epoch
cfg = {
        # height, in_ch, mid_ch, out_ch, RSU4F, side
        "encode": [[7, 3, 32, 64, False, False],      # En1
                   [6, 64, 32, 128, False, False],    # En2
                   [5, 128, 64, 256, False, False],   # En3
                   [4, 256, 128, 512, False, False],  # En4
                   [4, 512, 256, 512, True, False],   # En5
                   [4, 512, 256, 512, True, True]],   # En6
        # height, in_ch, mid_ch, out_ch, RSU4F, side
        "decode": [[4, 1024, 256, 512, True, True],   # De5
                   [4, 1024, 128, 256, False, True],  # De4
                   [5, 512, 64, 128, False, True],    # De3
                   [6, 256, 32, 64, False, True],     # De2
                   [7, 128, 16, 64, False, True]]     # De1
    }
batch_size = 4
epochs = 100
amp = False
resume = False
start_epoch = 0
print_freq = 50
eval_interval = 10

result_file = "results{}.txt".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
train_dataset = DUTSDataset("/911G/data/duts",train = True,
                                transforms = T.Compose([T.ToTensor(),]))

val_dataset = DUTSDataset("/911G/data/duts",train = False,
                              transforms = T.Compose([T.ToTensor(),]))

num_workers =  min([os.cpu_count(),batch_size if batch_size>1 else 0, 8])
train_data_loader = data.DataLoader(train_dataset,batch_size=batch_size,shuffle = True,num_workers = num_workers,pin_memory=True,collate_fn = train_dataset.collate_fn)
val_data_loader = data.DataLoader(val_dataset,batch_size = 1,shuffle = True,num_workers = num_workers,pin_memory=True,collate_fn = train_dataset.collate_fn)

model = U2Net(cfg)
model.to(device)


params_group = get_params_groups(model,weight_decay =1e-4 )
optimizer = torch.optim.AdamW(params_group,lr = 0.001,weight_decay = 1e-4)
lr_scheduler = create_lr_scheduler(optimizer,len(train_data_loader),epochs,warmup = True,warmup_epochs = 2)
scaler = torch.cuda.amp.GradScaler() if amp else None

if resume:
    checkpoint = torch.load(resume,map_location = 'cpu')
    model.load_state_dict(checkpoint['model'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    lr_scheduler.load_state_dict(checkpoint['lr_scheduler'])
    start_epoch = checkpoint['epoch'] +1
    if amp:
        scaler.load_state_dict(checkpoint['scaler'])

current_mae, current_f1 = 1.0, 0.0
start_time = time.time()
for epoch in range(start_epoch,epochs):
    mean_loss, lr = train_one_epoch(model, optimizer, train_data_loader, device, epoch, lr_scheduler = lr_scheduler,
                                    print_freq = print_freq, scaler = scaler)

    save_file = {"model":model.state_dict(),
                 "optimizer":optimizer.state_dict(),
                 "lr_scheduler":lr_scheduler.state_dict(),
                 "epoch":epoch}
    if amp:
        save_file["scaler"] = scaler.state_dict()

    if epoch % eval_interval == 0 or epoch == epochs -1:
        mae_metric, f1_metric = evaluate(model, val_data_loader,device = device)
        mae_info, f1_info = mae_metric.compute(), f1_metric.compute()
        print(f"[epoch: {epoch}] val_MAE: {mae_info:.3f} val_maxF1: {f1_info:.3f}")
        with open(results_file,"a") as f:
            write_info = f"[epoch: {epoch}] trin_loss: {mean_loss:.4f} lr:{lr:.6f} MAE: {mae_info:.3f} maxF1: {f1_info:.3f}"
            f.write(write_info)
        
        if current_mae >= mae_info and current_f1 <= f1_info:
            torch.save(save_file, "save_weights/model_best.pth")
    
    if os.path.exists(f"save_weights/model_{epoch-10}.pth"):
        os.remove(f"save_weights/model_{epoch-10}.pth")
    torch.save(save_file,f"save_weights/model_{epoch}.pth")

total_time = time.time() -start_time
total_time_str = str(datetime.timedelta(seconds = int(total_time)))
print("trianing time {}".format(total_time_str))




