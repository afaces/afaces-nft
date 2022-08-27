from PIL import Image
import numpy as np

class CustomImage:
    imageArray = [] # List of 3 elements

    def __init__(self, path):
        self.image = np.array(Image.open(path))

    def saveImage(self, path):
        Image.fromarray(self.image).save(path)

    def changeColor(self, rgb_pick, rgb_substitute):
        for i in range(len(self.image)):
            for j in range (len(self.image[i])):
                k = 0
                equal = True
                while k < len(self.image[i][j]):
                    print('olaa', self.image[i][j][k])
                    if self.image[i][j][k] != rgb_substitute[k]:
                        equal = False
                    k += 1

                if equal:
                    print("olanamamam")
                    self.image[i][j] = rgb_substitute


if __name__ == '__main__':
    customImage = CustomImage(f'./input/skeletons/ske_white.png')
    customImage.changeColor((253, 253, 253, 0), (69, 69, 69, 0))
    customImage.saveImage("./output/ske_white_.png")