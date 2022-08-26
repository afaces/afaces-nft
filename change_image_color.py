import numpy as np
from PIL import Image

def change_color(im, rgb_pick, rgb_substitute, output_name):

    data = np.array(im)
    r1, g1, b1 = rgb_pick[0], rgb_pick[1], rgb_pick[2] # Original value
    r2, g2, b2 = rgb_substitute[0], rgb_substitute[1], rgb_substitute[2] # Value that we want to replace it with

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:, :, :3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save(output_name)

image = Image.open(f'./input/skeletons/ske_white.png')


rgb = []
rgba = []
for i in range(0, 254):
    rgba.append(i)
    for j in range(0, 254):
        for k in range(0, 254):
            rgb.append(str(i) + ", " + str(j) + ", " + str(k))


for color in rgb:
    rgbColor = color.split(", ")
    r = rgbColor[0]
    g = rgbColor[1]
    b = rgbColor[2]
    original_color = (r, g, b)

    for aaa in rgba:
        a = str(aaa)
        replace_color = (int(r), int(g), int(b), int(a))
        name = "./output/ske_white_" + str(r) + str(g) + str(b) + str(a) + ".png"
        if int(a) < 2:
            change_color(image, original_color, replace_color, name)

