import matplotlib.pyplot as plt
import czifile
import scratch_test_class as st
from skimage.segmentation import mark_boundaries

ST = st.Scratch_test()
ST.setImages('/home/pmk/for/ibmh/hacat 2021/tgfb/photo/last/github')
ST.setTargets('0d_k')
ST.setTargetThreshold()
ST.count_scratch_area()
ST.display(ncols=3)

fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(50, 50))       
for ax, b, i, title in zip(axes.flatten(), ST.binaries, ST.images, ST.imagenames):
    ax.imshow(czifile.imread(i)[0,:,:,0], cmap='gray')
    ax.imshow(b, cmap='Greens_r', alpha=0.5)
    ax.axis('off')
    ax.set_title(title, fontsize=50)
fig.tight_layout()

fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(50, 50))       
for ax, b, i, title in zip(axes.flatten(), ST.binaries, ST.images, ST.imagenames):
    ax.imshow(mark_boundaries(czifile.imread(i)[0,:,:,0], 
                               b, 
                               color=(0, 1, 0), 
                               outline_color=(1, 1, 0),
                               mode = 'thick'))
    ax.axis('off')
    ax.set_title(title, fontsize=50)
fig.tight_layout()