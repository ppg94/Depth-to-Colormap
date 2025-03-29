import cv2
import os
scr_dir = 'F:\Surt_colmap\depth\scr'
out_dir = 'F:\Surt_colmap\depth\output'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
def convertdep():

    for idx,pic in enumerate(os.listdir(scr_dir)): 
        src_path = os.path.join(scr_dir, pic) 
        depth = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)  
        color_img = cv2.applyColorMap(depth,cv2.COLORMAP_PLASMA)
        cv2.imwrite(os.path.join(out_dir,f"{idx}.png"),color_img)

convertdep()
