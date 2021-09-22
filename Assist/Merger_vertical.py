import numpy as np
import PIL
import os
import fnmatch

from PIL import Image

location = 'C:/Users/Max/OneDrive/BlenderProjects/Planets/Moon'

main_folders = []

for folder in os.listdir(location):
    main_folders.append(location + '/' + folder)

for folder in main_folders:

    image_list = []

    for filename in fnmatch.filter(os.listdir(folder), "*.jpg"):
        image_list.append(folder + '/' + filename)

    image_list.sort(key=lambda sorter: int(sorter.split('/')[8].strip(' row.jpg')))
    images = [PIL.Image.open(i) for i in image_list]

    images_combined = np.vstack(images)
    images_combined = PIL.Image.fromarray(images_combined)
    images_combined.save(folder + '.jpg')
