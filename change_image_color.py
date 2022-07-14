import numpy as np
from PIL import Image

def change_color(im, rgb_pick, rgb_substitute):

    data = np.array(im)
    r1, g1, b1 = rgb_pick[0], rgb_pick[1], rgb_pick[2] # Original value
    r2, g2, b2 = rgb_substitute[0], rgb_substitute[1], rgb_substitute[2] # Value that we want to replace it with

    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save('ske_white_modified.png')

image = Image.open(f'./input/skeletons/ske_white.png')

original_color = (253, 253, 253) # White
replace_color = (0, 0, 0, 0) # Black


change_color(image, original_color, replace_color)

