from PIL import Image
from IPython.display import display
import shutil
import random
import json
import os


def create_new_image():
    new_image = {}
    new_image["Background"] = random.choices(backgrounds, backgrounds_weights)[0]
    new_image["Eye"] = random.choices(eyes, eyes_weights)[0]
    new_image["Skin"] = random.choices(skins, skins_weights)[0]
    new_image["Mouth"] = random.choices(mouths, mouths_weights)[0]
    new_image["Tie"] = random.choices(ties, ties_weights)[0]
    new_image["Skeleton"] = random.choices(skeletons, skeletons_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image

# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


# Change image color
# Save different max and min sizes of body parts


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

backgrounds = ["Black", "White"]
backgrounds_weights = [20, 80]
backgrounds_files = {
    "Black": "bg_black",
    "White": "bg_white",
}
backgrounds_count = {}
for bg in backgrounds:
    backgrounds_count[bg] = 0

eyes = ["Black", "White"]
eyes_weights = [70, 30]
eyes_files = {
    "Black": "ey_black",
    "White": "ey_white",
}
eyes_count = {}
for ey in eyes:
    eyes_count[ey] = 0

skins = ["Black", "White"]
skins_weights = [40, 60]
skins_files = {
    "Black": "ski_black",
    "White": "ski_white",
}
skins_count = {}
for ski in skins:
    skins_count[ski] = 0

mouths = ['Black', 'White']
mouths_weights = [10, 90]
mouths_files = {
    "Black": "mo_black",
    "White": "mo_white",
}
mouths_count = {}
for mo in mouths:
    mouths_count[mo] = 0

ties = ["Red", "Yellow", "Green"]
ties_weights = [90, 6, 4]
ties_files = {
    "Red": "ti_red",
    "Yellow": "ti_yellow",
    "Green": "ti_green",
}
ties_count = {}
for ti in ties:
    ties_count[ti] = 0

skeletons = ["Black", "White"]
skeletons_weights = [99, 1]
skeletons_files = {
    "Black": "ske_black",
    "White": "ske_white",
}
skeletons_count = {}
for ske in skeletons:
    skeletons_count[ske] = 0

# Generate traits:

TOTAL_IMAGES = 47

all_images = []


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)


print("Are all images unique?", all_images_unique(all_images))
# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

print(all_images)

for image in all_images:
    backgrounds_count[image["Background"]] += 1
    eyes_count[image["Eye"]] += 1
    skins_count[image["Skin"]] += 1
    mouths_count[image["Mouth"]] += 1
    ties_count[image["Tie"]] += 1
    skeletons_count[image["Skeleton"]] += 1

print(backgrounds_count)
print(eyes_count)
print(skins_count)
print(mouths_count)
print(ties_count)
print(skeletons_count)

#### Generate Images
shutil.rmtree("./output")
os.mkdir(f'./output')

for item in all_images:
    im1 = Image.open(f'./input/backgrounds/{backgrounds_files[item["Background"]]}.png').convert('RGBA')
    im2 = Image.open(f'./input/eyes/{eyes_files[item["Eye"]]}.png').convert('RGBA')
    im3 = Image.open(f'./input/skins/{skins_files[item["Skin"]]}.png').convert('RGBA')
    im4 = Image.open(f'./input/mouths/{mouths_files[item["Mouth"]]}.png').convert('RGBA')
    im5 = Image.open(f'./input/ties/{ties_files[item["Tie"]]}.png').convert('RGBA')
    im6 = Image.open(f'./input/skeletons/{skeletons_files[item["Skeleton"]]}.png').convert('RGBA')


    # Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)

    # Convert to RGB
    rgb_im = com5.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./output/" + file_name)

