import numpy as np
import cv2
import os
from PIL import Image



names = ["brody"]
names.append("clarke")
names.append("derya")
names.append("fassbender")
names.append("hussam")
names.append("keira")
names.append("kit")
names.append("leo")
names.append("matt")
names.append("morgan")
names.append("natalie")
names.append("abdullah")
names.append("mnzr")

names.sort()
print(names)


i = 0

images = []
labels = []


for name in names:
	path = "dataset\\" + name
	imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
	for imagePath in imagePaths:
		if imagePath.split(".")[-1] != "jpg":
			continue
		print(imagePath + " *** \t" + name + ": " + str(i))
		#image_pil = Image.open("dataset\\" + names[i] + "\\" + names[i] + " (" + str(count) +  ").jpg").convert('L')
		image_pil = Image.open(imagePath).convert('L')
		image = np.array(image_pil, 'uint8')
		images.append(image)
		labels.append(i+1)
	i = i+1
recognizer.train(images, np.array(labels))
recognizer.save('trainningData.yml')

	

cv2.destroyAllWindows()



