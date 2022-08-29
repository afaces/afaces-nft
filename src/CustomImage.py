from PIL import Image
import numpy as np


class CustomImage:
    def __init__(self, path):
        if path is None:
            self.image = None
            return
        self.image = np.array(Image.open(path))

    def copy(self):
        ima = CustomImage(None)
        ima.image = self.image.copy()
        return ima

    def save_image(self, path):
        Image.fromarray(self.image).save(path)

    # Changes the internal color of the inner image
    def change_color(self, rgb_pick, rgb_substitute):
        r1, g1, b1 = rgb_pick[0], rgb_pick[1], rgb_pick[2]  # Original value
        r2, g2, b2 = rgb_substitute[0], rgb_substitute[1], rgb_substitute[2]  # Value that we want to replace it with

        red, green, blue = self.image[:, :, 0], self.image[:, :, 1], self.image[:, :, 2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        self.image[:, :, :3][mask] = [r2, g2, b2]

    @staticmethod
    # Changes the color of the received image
    def change_color_static(custom_image, rgb_pick, rgb_substitute):
        r1, g1, b1 = rgb_pick[0], rgb_pick[1], rgb_pick[2]  # Original value
        r2, g2, b2 = rgb_substitute[0], rgb_substitute[1], rgb_substitute[2]  # Value that we want to replace it with

        custom_image_array = custom_image.image
        red, green, blue = custom_image_array[:, :, 0], custom_image_array[:, :, 1], custom_image_array[:, :, 2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        custom_image_array[:, :, :3][mask] = [r2, g2, b2]

        custom_image = CustomImage(None)
        custom_image.image = custom_image_array
        return custom_image

    def do_composite(self, images_list):
        im = Image.fromarray(self.image).convert('RGBA')
        for image in images_list:
            im = Image.alpha_composite(im, Image.fromarray(image.image).convert('RGBA'))
        self.image = np.array(im.convert('RGB'))

    # Receives a list of paths to images that want to be composed, or receives directly image data, and returns a
    # CustomImage instance with the result
    @staticmethod
    def do_composite_static(images_list):
        im = None
        if type(images_list[0]) is CustomImage:  # Assuming image data
            im = Image.fromarray(images_list[0].image).convert('RGBA')
            for image in images_list[1:]:
                im = Image.alpha_composite(im, Image.fromarray(image.image).convert('RGBA'))
        else:  # Assuming paths
            im = Image.open(images_list[0]).convert('RGBA')
            for image in images_list[1:]:
                im = Image.alpha_composite(im, Image.open(image).convert('RGBA'))

        custom_image = CustomImage(None)
        custom_image.image = np.array(im)
        return custom_image

