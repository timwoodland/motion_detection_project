import cv2
import glob

images = glob.glob("sample_images/*.jpg")

new_size =(100, 100)

for i in images:
    image = cv2.imread(i, 1)
    image_resized = cv2.resize(image, new_size)
    name = i.split("\\")
    name = name[1]
    name = name[:-4]
    name_formatted = "output\\{name}_resized.jpg".format(name = name)
    cv2.imwrite(name_formatted, image_resized)

