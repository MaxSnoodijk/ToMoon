from PIL import Image
import numpy as np

width, height = 16384, 8192
data = np.random.rand(height, width)

rows = np.where(data < 0.0001)[0]
columns = np.where(data < 0.0001)[1]

color_data = np.zeros((height, width), np.uint8)

for i in range(len(rows)):

    color_data[rows[i], columns[i]] = 255

img = Image.fromarray(color_data)
img.save('SkyTexture.png')
img.show()
