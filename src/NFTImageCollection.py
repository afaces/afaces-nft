# from PIL import Image
import random

import numpy as np
import os
import shutil
from CustomImage import CustomImage
from IndexIterator import IndexIterator
from pathlib import Path


# Contains the necessary data and functions
class NFTImageCollection:
    # Number used to increase the RGB value for each RGB iteration
    RGB_STEP = 127  # With 127 We get 3 values: 0, 128, 254 --> 3 ^ 3 = 27 combs of colour
    DEFAULT_INPUT = (253, 253, 253)

    # Generate the list of trait names from the names of the folder inside self.DATA_FOLDER_PATH and initializes
    # NFTCollection object
    def __init__(self, trait_folder_names):
        # Obtain absolute path location
        # This return absolute path to the file we are running
        self.BASE_PATH = str(Path(os.path.realpath(__file__)).parent.parent)

        self.DATA_FOLDER_PATH = os.path.join(self.BASE_PATH, "data")
        self.TEMPORAL_FOLDER_PATH = os.path.join(self.BASE_PATH, "tmp")
        self.OUTPUT_FOLDER_PATH = os.path.join(self.BASE_PATH, "out")

        # Initialize data
        if trait_folder_names is None:
            self.traitNameList = os.listdir(self.DATA_FOLDER_PATH)
        else:
            self.traitNameList = trait_folder_names
        self.traitFilesVariationsDictionary = {}

        # Generate output file structure
        shutil.rmtree(self.TEMPORAL_FOLDER_PATH, ignore_errors=True)
        os.mkdir(self.TEMPORAL_FOLDER_PATH)
        shutil.rmtree(self.OUTPUT_FOLDER_PATH, ignore_errors=True)
        os.mkdir(self.OUTPUT_FOLDER_PATH)
        for traitName in self.traitNameList:
            os.mkdir(os.path.join(self.TEMPORAL_FOLDER_PATH, traitName))

    # Fills self.traitFilesVariationsDictionary with each trait file, generated from the RGB variations of the trivial
    # trait variation in each trait folder, which has been decided to be "0_20.png". So, this functions needs a
    # "0_20.png" file in each folder in self.DATA_FOLDER_PATH. This 1_23.png file has to be white with 255 for each RGB
    # value. The generated files will be located in self.OUTPUT_FOLDER_PATH/traitName/RedValue_GreenValue_BlueValue.png
    def generate_trait_files_rgb(self):
        for traitName in self.traitNameList:
            current_trivial_trait_image = CustomImage(os.path.join(self.DATA_FOLDER_PATH, traitName, "_.png"))
            self.traitFilesVariationsDictionary[traitName] = []
            for r in range(0, 256, self.RGB_STEP):
                for g in range(0, 256, self.RGB_STEP):
                    for b in range(0, 256, self.RGB_STEP):
                        print("Variating trait " + str(traitName) + " with RGB code (" + str(r)+ ", " + str(g) + ", " + str(b) + ")")
                        current_image = CustomImage.change_color_static(current_trivial_trait_image, self.DEFAULT_INPUT, (r, g, b))
                        file_path = os.path.join(self.TEMPORAL_FOLDER_PATH, traitName, str(r) + "_" + str(g) + "_" + str(b) + ".png")
                        self.traitFilesVariationsDictionary[traitName].append([file_path, 1])
                        current_image.save_image(file_path)

    # Fills self.traitFilesVariationsDictionary with each trait name from self.traitNameList as key with the
    # trivial variation (0_20.png)
    def generate_trait_files_trivial(self):
        for traitName in self.traitNameList:
            self.traitFilesVariationsDictionary[traitName] = []
            for filename in os.listdir(os.path.join(self.DATA_FOLDER_PATH, traitName, "weighted")):
                input_path = os.path.join(self.DATA_FOLDER_PATH, traitName, "weighted", filename)
                out_filename = filename.split("_")[0] + ".png"  # Obtain the part before the _ from the file
                absolute_frequency = int(filename.split(".")[0].split("_")[1])

                output_path = os.path.join(self.TEMPORAL_FOLDER_PATH, traitName, out_filename)
                shutil.copyfile(input_path, output_path)
                self.traitFilesVariationsDictionary[traitName].append([output_path, absolute_frequency])

    def compute_relative_probability(self):
        for traitName in self.traitNameList:
            sum_trait = 0
            for traitVariation in self.traitFilesVariationsDictionary[traitName]:
                sum_trait += traitVariation[1]
            for traitVariation in self.traitFilesVariationsDictionary[traitName]:
                traitVariation[1] /= sum_trait

    # Generate each variation using all traits selected, ignore probability
    def generate_repeat_variations(self):
        index_iterator = IndexIterator(self.traitFilesVariationsDictionary)

        num_variations = 1
        while index_iterator.has_next():
            current_images = []
            name = str(num_variations) + "_"
            print("\nVariation " + str(num_variations) + " using combination of varying traits " + str(index_iterator))
            for traitName in self.traitFilesVariationsDictionary.keys():
                print(self.traitFilesVariationsDictionary[traitName][index_iterator.currentValues[traitName]][0])
                name += traitName + "_" + self.traitFilesVariationsDictionary[traitName][index_iterator.currentValues[traitName]][0].split("/")[-1].split(".")[0] + "__"
                current_images.append(self.traitFilesVariationsDictionary[traitName][index_iterator.currentValues[traitName]][0])

            CustomImage.do_composite_static(current_images).save_image(os.path.join(self.OUTPUT_FOLDER_PATH, name + ".png"))
            index_iterator.next()
            num_variations += 1

    def generate_weighted_variations(self, num):
        counter = 1
        while counter <= num:
            current_images = []
            name = ""
            for key in self.traitFilesVariationsDictionary.keys():
                current_weights = []
                for traitVariation in self.traitFilesVariationsDictionary[key]:
                    current_weights.append(traitVariation[1])

                chosen_path = random.choices(self.traitFilesVariationsDictionary[key], current_weights)[0][0]
                name += key + "_" + chosen_path.split("/")[-1].split(".")[0] + "__"
                current_images.append(chosen_path)

            print("Variation " + str(counter) + ": " + str(name))
            CustomImage.do_composite_static(current_images).save_image(os.path.join(self.OUTPUT_FOLDER_PATH, name + ".png"))
            counter += 1


def generate_rgb_repeat_variations():
    nftCollection = NFTImageCollection(['background', 'eye', 'skin', 'mouth', 'tie', 'skeleton'])
    nftCollection.generate_trait_files_rgb()  # NFTCollection.generate_trait_files_trivial()
    nftCollection.compute_relative_probability()
    nftCollection.generate_repeat_variations()


def generate_weighted_combinations(num_variations):
    nftCollection = NFTImageCollection(['background', 'eye', 'skin', 'mouth', 'tie', 'skeleton'])
    nftCollection.generate_trait_files_trivial()
    nftCollection.compute_relative_probability()
    nftCollection.generate_weighted_variations(num_variations)


def generate_rgb_weighted_variations(num_variations):
    nftCollection = NFTImageCollection(['background', 'eye', 'skin', 'mouth', 'tie', 'skeleton'])
    nftCollection.generate_trait_files_rgb()
    nftCollection.compute_relative_probability()
    nftCollection.generate_weighted_variations(num_variations)


if __name__ == '__main__':
    # generate_rgb_repeat_variations()
    # generate_weighted_combinations(100)
    generate_rgb_weighted_variations(100)