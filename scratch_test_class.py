import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.filters.rank import entropy
from skimage.filters import gaussian, threshold_triangle
from skimage.morphology import reconstruction
import czifile
import os
import re

class Scratch_test:
    def __init__(self):
        self.im_dir = "no dir"
        self.images = "no images"
        self.imagenames = 'no imagenames'
        self.results = []
        self.target_names = 'no targets'
        self.target_positions = 'no targets'
        self.target_images = 'no targets'
        self.target_threshold = 'no target threshold'
        self.mean_target_threshold = "no threshold"
        self.area = 'not counted'
        self.binaries = 'not counted'
        self.fig = 'not created'
        
    def setImages(self, im_dir, pattern = r'.*/(.*)/(.*)/(.*)\.czi', feedback = r'\1_\2_'):
        self.images, self.imagenames = tuple(zip(*((os.path.join(root, filename), 
                                                    re.sub(pattern, feedback+'rep{}'.format(index), os.path.join(root, filename)).lower())
                                                    for root, dirs, files in os.walk(im_dir)
                                                    for index, filename in enumerate(files)
                                                    if filename.lower().endswith('.czi'))))
        
    def setTargets(self, targets = "0d_k"):
        self.target_names = [im for im in self.imagenames if re.search(targets, im)]
        self.target_positions = [i for i, j in enumerate(self.imagenames) if j in  self.target_names]
        self.target_images = [self.images[i] for i in self.target_positions]
    
    def setTargetThreshold(self, disk_num = 5, offset = 0):
        self.target_threshold = []
        for image in self.target_images:
            pic = czifile.imread(image)
            pics_entr = entropy(pic[0,:,:,0], np.ones((30, 30)))
            pics_entr = gaussian(pics_entr, sigma = 15)
            mask = pics_entr
            seed = np.copy(pics_entr)
            seed[1:-1, 1:-1] = pics_entr.min()
            rec = reconstruction(seed, mask, method='dilation')
            self.target_threshold.append(threshold_triangle(rec))
        self.mean_target_threshold = np.mean(self.target_threshold) + offset
        
    def count_scratch_area(self):
        self.area = []
        self.binaries = []
        l=len(self.images)
        for index, image in enumerate(self.images):
            pic = czifile.imread(image)
            print(f"{index} of {l} images")
            pics_entr = entropy(pic[0,:,:,0], np.ones((20, 20)))
            pics_entr = gaussian(pics_entr, sigma = 10)
            mask = pics_entr
            seed = np.copy(pics_entr)
            seed[1:-1, 1:-1] = pics_entr.min()
            rec = reconstruction(seed, mask, method='dilation')
            binary = rec <= self.mean_target_threshold
            bin_sum = np.sum(binary)
            self.binaries.append(binary)
            self.area.append(bin_sum)
        print('Done!')
        
    def save_df_to_csv(self, df_dir):
        pd.DataFrame({'name': self.imagenames, 'area': self.area}).to_csv(df_dir, index = False)
        
    def display(self, cmap="gray", title = None, ncols=8):
        self.fig, axes = plt.subplots(ncols=ncols, nrows=len(self.binaries)//ncols, figsize=(50, 50))
        for ax, image, tit in zip(axes.flatten(), self.binaries, self.imagenames):
            ax.imshow(image, cmap=cmap)#vmin=vmin, vmax=vmax
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(tit, fontsize=50)
        self.fig.tight_layout()
        
    def count_all(self, im_dir, targets = "0d_k"):
        self.setImages(im_dir = im_dir)
        self.setTargets(targets)
        self.setTargetThreshold()
        self.count_scratch_area()
        self.display()
