#autil.py
import glob 
import torch
import os


def accum_section_track(section, load_path):

  initial_load = torch.load(load_path+'/track1.pth')
  accum_track = dict([(k, torch.zeros_like(v)) for k, v in initial_load.items()])

  for i in range(section[0]+1,  section[1]+1):
    path = load_path + '/track'+str(i)+'.pth'
    track_load = torch.load(path)
    for k, v in track_load.items():
      accum_track[k] += v
  
  save_path = load_path+'/track_section'+str(section[0])+'_'+str(section[1])
  if not os.path.isdir(save_path):
    os.mkdir(save_path)
  
  print(accum_track.keys())
  torch.save(accum_track, save_path+'/track.pth')





def make_mask_sub(tracked_bin, mixed_portion):
  
  size = tracked_bin.size()
  
  flat = tracked_bin.reshape([-1, ])
  p = int(len(flat)*mixed_portion)
  v, idx = flat.topk(k=p)
  threshold = v[p-1]
  
  mask = torch.where(flat > threshold, torch.ones_like(flat), torch.zeros_like(flat))

  return mask.reshape(size)

def make_mask(load_path, mixed_portion):
  bin_change = torch.load(load_path+'/track.pth')

  mask = dict([(k, make_mask_sub(v[1], mixed_portion)) for k, v in enumerate(bin_change.items())])


  torch.save(mask, load_path+'/mask_'+str(mixed_portion)+'.pth')
  print('Make mask..')
  

