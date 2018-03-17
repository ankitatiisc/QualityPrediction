from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.layers import Input,Flatten,Dense
from keras.models import Model
from keras.applications.inception_v3 import preprocess_input
import numpy as np

def create_vgg_16_model():
	#Get feature extractor of VGG16 trained on imagenet dataset
	vgg_model_conv = VGG16(weights='imagenet',include_top=False)
	for layers in vgg_model_conv.layers:
		#print(layers)
		layers.trainable = False
	#vgg_model_conv.summary()
	
	input = Input(shape=(256,256,3),name = 'image_input')

	vgg_model_conv.layers[-1].trainable=True
	vgg_model_conv.layers[-2].trainable=True
	#Use the generated model 
	vgg16_conv_out = vgg_model_conv(input)

	#fully-connected layers 
	x = Flatten(name='flatten')(vgg16_conv_out)
	x = Dense(32, activation='relu', name='fc1')(x)
	x = Dense(16, activation='relu', name='fc2')(x)
	x = Dense(2, activation='softmax', name='predictions')(x)

	#Create your own model 
	model = Model(input=input, output=x)

	model.summary()

	return model
	
def create_inception_v3_model():
	inception_conv = InceptionV3(include_top=False,weights='imagenet')
	input = Input(shape=(299,299,3),name = 'image_input')

	#Use the generated model 
	inception_conv_out = inception_conv(input)

	#fully-connected layers 
	x = Flatten(name='flatten')(inception_conv)
	x = Dense(32, activation='relu', name='fc1')(x)
	x = Dense(16, activation='relu', name='fc2')(x)
	x = Dense(2, activation='softmax', name='predictions')(x)

	#Create your own model 
	model = Model(input=input, output=x)

	model.summary()

	return model
