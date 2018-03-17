from keras.optimizers import SGD,Adagrad,Adam
from keras.utils import to_categorical

from train_images import create_vgg_16_model
from data_processing import load_images,data_generator

from keras.models import load_model
from keras.callbacks import ModelCheckpoint 

import argparse 
import numpy as np

parser =  argparse.ArgumentParser()

parser.add_argument("imgs_list",help="path of txt file containing images")

parser.add_argument("-m","--model", help="path to the model")

args = parser.parse_args() 

if args.model is None:
	train_model = create_vgg_16_model()
else:
	print('Loading model from the previous weights')
	train_model = load_model(args.model)

#Compile the model
sgd = SGD(lr=0.000001, decay=1e-6, momentum=0.9, nesterov=True)
adagrad = Adagrad()
adam = Adam(lr=0.000001)
train_model.compile(loss='categorical_crossentropy',optimizer=adagrad,metrics=['accuracy'])

img_shape = (256,256)
#Load data

#X,Y = load_images(args.imgs_list, img_shape)
file_ = open(args.imgs_list,'r')
imgs_list = file_.readlines()
file_.close()

print('Loaded {} images'.format(len(imgs_list)))

#label_categorical = to_categorical(Y, num_classes=2)

#train_model.fit(X, label_categorical, batch_size=32, epochs=50)
saver = ModelCheckpoint('first_model_bestSwag.h5', monitor='loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)
batch_size = 32
train_model.fit_generator(data_generator(imgs_list,img_shape,batch_size),steps_per_epoch=len(imgs_list)/batch_size, epochs=1000, verbose=1,callbacks =[saver])

train_model.save('first_model.h5')




