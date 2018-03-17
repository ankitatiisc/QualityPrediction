from keras.optimizers import SGD
from keras.utils import to_categorical
from keras.models import load_model
from keras.metrics import categorical_accuracy

from data_processing import load_images

import argparse 
import numpy as np

from sklearn.metrics import confusion_matrix

parser =  argparse.ArgumentParser()

parser.add_argument("model",help="path of model")
parser.add_argument("imgs_list",help="path of txt file containging images")


args = parser.parse_args() 

model = load_model(args.model)	

#Compile the model
#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#train_model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])

img_shape = (256,256)
#Load data

X,Y = load_images(args.imgs_list, img_shape)
print('Loaded {} images'.format(X.shape[0]))

Y_pred = model.predict(X)

#Y = to_categorical(Y, num_classes=2)



Y_pred = Y_pred.argmax(1)


#print(Y)
#print(Y_pred)

res = confusion_matrix(Y,Y_pred)

print("Confusion matrix:\n%s" % res)

print("tn fp fn tp : {}\n".format(res.ravel()))
