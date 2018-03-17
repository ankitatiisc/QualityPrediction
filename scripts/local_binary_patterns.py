# import the necessary packages
from skimage import feature
import numpy as np
from sklearn.svm import LinearSVC
import argparse
from PIL import Image
import cPickle

class LocalBinaryPatterns:
	def __init__(self, numPoints, radius):
		# store the number of points and radius
		self.numPoints = numPoints
		self.radius = radius

	def describe(self, image, eps=1e-7):
		# compute the Local Binary Pattern representation
		# of the image, and then use the LBP representation
		# to build the histogram of patterns
		lbp = feature.local_binary_pattern(image, self.numPoints,
			self.radius, method="uniform")
		(hist, _) = np.histogram(lbp.ravel(),
			bins=np.arange(0, self.numPoints + 3),
			range=(0, self.numPoints + 2))

		# normalize the histogram
		hist = hist.astype("float")
		hist /= (hist.sum() + eps)

		# return the histogram of Local Binary Patterns
		return hist

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("imgs_list",help="path of txt file containing images")

args = ap.parse_args()

# initialize the local binary patterns descriptor along with
# the data and label lists
desc = LocalBinaryPatterns(24, 8)
data = []
labels = []
#X,Y = load_images(args.imgs_list, img_shape)
file_ = open(args.imgs_list,'r')
imgs_list = file_.readlines()
file_.close()

img_size = (640,480)

# loop over the training images
count = 0
print("Preparing data")
for line in imgs_list:
    
    temp = line.split()
    #print(temp)
    img_path = temp[0]
    label = int(temp[1])
    if label == 0 :
        label = 1
    else:
        label = 0
	# load the image, convert it to grayscale, and describe it
    image = Image.open(img_path)
    if image is None:
        continue
    gray = image.convert("L")
    rsz_img = gray.resize(img_size,Image.NEAREST)
    hist = desc.describe(np.asarray(rsz_img))

    # extract the label from the image path, then update the
    # label and data lists
    labels.append(label)
    data.append(hist)

print("Training model")
# train a Linear SVM on the data
model = LinearSVC(C=100.0, random_state=42)
model.fit(data, labels)


print("saving model")
# save the classifier
with open('linear_svc.pkl', 'wb') as fid:
    cPickle.dump(model  , fid)

# load it again
with open('linear_svc.pkl', 'rb') as fid:
    model_loaded = cPickle.load(fid)
