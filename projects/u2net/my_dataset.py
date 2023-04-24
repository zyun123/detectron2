import cv2
import torch.utils.data as data
import os
import numpy as np
import transforms as T



class DUTSDataset(data.Dataset):
    def __init__(self,root,train = True,transforms = None):
        assert os.path.exists(root), f"{root} does not exist."
        if train:
            self.image_root = os.path.join(root, "DUTS-TR", "DUTS-TR-Image")
            self.mask_root = os.path.join(root,"DUTS-TR", "DUTS-TR-Mask")
        else:
            self.image_root = os.path.join(root,"DUTS-TE", "DUTS-TE-Image")
            self.mask_root = os.path.join(root,"DUTS-TE", "DUTS-TE-Mask")
        assert os.path.exists(self.image_root),f"path {self.image_root} does not exist"
        assert os.path.exists(self.mask_root),f"path {self.mask_root} does not exist"

        image_names = [p for p in os.listdir(self.image_root) if p.endswith(".jpg")]
        mask_names = [p for p in os.listdir(self.mask_root) if p.endswith(".png")]
        assert len(image_names) >0, f"not find any images in {self.image_root}"

        re_mask_names = []
        for p in image_names:
            mask_name = p.replace(".jpg",".png")
            assert mask_name in mask_names,f"{p} has no corresponding mask"
            re_mask_names.append(mask_name)
        mask_names = re_mask_names

        self.images_path = [os.path.join(self.image_root,n) for n in image_names]
        self.masks_path = [os.path.join(self.mask_root,n) for n in mask_names]

        self.transforms = transforms

    def __getitem__(self,idx):
        image_path = self.images_path[idx]
        mask_path = self.masks_path[idx]
        image = cv2.imread(image_path,flags = cv2.IMREAD_COLOR)
        assert image is not None, "failed to read image"
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        h,w,_ = image.shape 

        target = cv2.imread(mask_path,flags = cv2.IMREAD_GRAYSCALE)
        assert target is not None, f"failed to read mask"

        if self.transforms is not None:
            image,target = self.transforms(image,target)    
        
        return image,target
    

    def __len__(self):
        return len(self.images_path)
    
    @staticmethod
    def collate_fn(batch):
        images,targets = list(zip(*batch))
        batched_imgs = cat_list(images,fill_value = 0)
        batched_targets = cat_list(targets,fill_value = 0)

        return batched_imgs, batched_targets
    

def cat_list(images,fill_value = 0):
    max_size  = tuple(max(s) for s in zip(*[img.shape for img in images]))
    batch_shape = (len(images),) + max_size
    batched_imgs = images[0].new(*batch_shape).fill_(fill_value)
    # batched_imgs = np.zeros(batch_shape)
    for img, pad_img in zip(images,batched_imgs):
        pad_img[...,:img.shape[-2],:img.shape[-1]].copy_(img)

    return batched_imgs


if __name__ == "__main__":
    train_dataset = DUTSDataset("/911G/data/duts",train = True,
                                transforms = T.Compose([T.ToTensor(),]))
    print(len(train_dataset))

    val_dataset = DUTSDataset("/911G/data/duts",train = False,
                              transforms = T.Compose([T.ToTensor(),]))
    print(len(val_dataset))

    i,t = train_dataset[0]
    
    batch_size =4
    num_workers = min([os.cpu_count(), batch_size if batch_size>1 else 0, 8])
    train_data_loader = data.DataLoader(train_dataset,
                                        batch_size = batch_size,
                                        num_workers = num_workers,
                                        shuffle = True,
                                        pin_memory = True,
                                        collate_fn = train_dataset.collate_fn)
    # images,targets = iter(train_data_loader).next()
    for image, target in train_data_loader:
        print(image.shape)
        print(target.shape)
        print("hhh")
