import numpy as np
import PIL
import os
import fnmatch

from PIL import Image

location = 'C:/Users/Max/OneDrive/BlenderProjects/Planets/Moon'

main_folders = []
sub_folders = []

for folder in os.listdir(location):
    main_folders.append(location + '/' + folder)

for i in range(len(main_folders)):
    for folder in os.listdir(main_folders[i]):
        sub_folders.append(main_folders[i] + '/' + folder)

for folder in sub_folders:

    image_list = []

    for filename in fnmatch.filter(os.listdir(folder), "*.jpg"):
        image_list.append(folder + '/' + filename)

    image_list.sort(key=lambda sorter: int(sorter.split('_')[3].strip('.jpg')))
    images = [PIL.Image.open(i) for i in image_list]

    images_combined = np.hstack(images)
    images_combined = PIL.Image.fromarray(images_combined)
    images_combined.save(folder + '.jpg')
