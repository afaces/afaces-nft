from PIL import Image
import numpy as np

RGB_STEP = 64

class CustomImage:
    image = None

    def __init__(self, path):
        if path is None:
            self.image = None
            return
        self.image = np.array(Image.open(path))

    def copy(self):
        ima = CustomImage(None)
        ima.image = self.image.copy()
        return ima


    def saveImage(self, path):
        Image.fromarray(self.image).save(path)

    def changeColor(self, rgb_pick, rgb_substitute):
        r1, g1, b1 = rgb_pick[0], rgb_pick[1], rgb_pick[2]  # Original value
        r2, g2, b2 = rgb_substitute[0], rgb_substitute[1], rgb_substitute[2]  # Value that we want to replace it with

        red, green, blue = self.image[:, :, 0], self.image[:, :, 1], self.image[:, :, 2]
        mask = (red == r1) & (green == g1) & (blue == b1)
        self.image[:, :, :3][mask] = [r2, g2, b2]

    def doComposite(self, images_list):
        im = Image.fromarray(self.image).convert('RGBA')
        for image in images_list:
            im = Image.alpha_composite(im, Image.fromarray(image.image).convert('RGBA'))
        self.image = np.array(im.convert('RGB'))


def generateRGB(path):
    for r in range(0, 256, RGB_STEP):
        for g in range(0, 256, RGB_STEP):
            for b in range (0, 256, RGB_STEP):
                customImage = CustomImage(path)
                customImage.changeColor((253, 253, 253), (r, g, b, 0))
                customImage.saveImage("./output/ske_" + str(r) + "_" + str(g) + "_" + str(b) + ".png")

def glueImages():
    traitsPaths = { "Backgrounds": "./input/backgrounds/bg_white.png",
                    "Eyes": "./input/eyes/ey_white.png",
                    "Skins": "./input/skins/ski_white.png",
                    "Mouths": "./input/mouths/mo_white.png"
                    #"Ties": "./input/ties/ti_red.png",
                    #"Skeletons": "./input/skeletons/ske_white.png"
                   }
    customImageList = []
    for traitsPaths in traitsPaths.values():
        customImageList.append(CustomImage(traitsPaths))

    customImageColorsList = []
    for k in range(len(customImageList)):
        print("pepe entrando")
        customImageColorsList.append([])
        for r in range(0, 256, RGB_STEP):
            for g in range(0, 256, RGB_STEP):
                for b in range(0, 256, RGB_STEP):
                    original_image = customImageList[k].copy()
                    customImageList[k].changeColor((253, 253, 253), (r, g, b))
                    customImageColorsList[k].append(customImageList[k])
                    customImageList[k] = original_image
    print("troleroo")
    print(len(customImageColorsList), "olaaaaaaaaaaaaaaaaaaa")

    index_array = []
    for _ in range(len(customImageColorsList)):
        index_array.append(0)
    print("KKK")
    for i in range(len(customImageColorsList) * RGB_STEP):
        print(str(index_array))
        currentCollage = []
        for j in range(len(index_array)):
            currentCollage.append(customImageColorsList[j][index_array[j]])
        currentCollage[0].doComposite(currentCollage[1:])
        currentCollage[0].saveImage("./output/" + str(index_array) + ".png")

        for g in range(len(index_array)):
            if index_array[g] < 256 / RGB_STEP - 1:
                index_array[g] += 1
                break
            else:
                k = g
                while(index_array[k] == 256 / RGB_STEP - 1):
                    index_array[k] = 0
                    if k < len(index_array):
                        k += 1
                        if k == len(index_array):
                            break
                    else:
                        break

                if k < len(index_array):
                    index_array[k] += 1
                break


if __name__ == '__main__':
    glueImages()