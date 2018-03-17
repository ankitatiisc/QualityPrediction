import numpy as np
from PIL import Image 
import pdb
from keras.utils import to_categorical

def load_images(img_list_file,img_size):
	file_ = open(img_list_file,'r')
	imgs_list = file_.readlines()
	file_.close()

	imgs_arr = np.empty((0,img_size[0],img_size[1],3),np.uint8)
	label_arr = np.empty((0,1),np.int32)
	for line in imgs_list:
		temp = line.split()
		#print(temp)
		img_path = temp[0]
		label = int(temp[1])
		if label == 0 :
			label = 1
		else:
			label = 0
		img = Image.open(img_path)
		if img is None:
			continue
		rsz_img = img.resize(img_size,Image.NEAREST)
		rsz_ = np.asarray(rsz_img).reshape((1,img_size[0],img_size[1],3))
		#print(rsz_.shape,imgs_arr.shape)
		imgs_arr = np.append(imgs_arr,rsz_,axis=0)
		#pdb.set_trace()
		arr_ = np.zeros((1,1))
		arr_[0] = label
		label_arr = np.append(label_arr,arr_,axis=0)

	return imgs_arr,label_arr

def data_generator(img_list,img_size,batch_size=32):
	imgs_arr = np.zeros((batch_size,img_size[0],img_size[1],3),np.uint8)
	#label_arr = np.empty((0,2),np.int32)
	
	tot_images = len(img_list)

	while 1:
		for i in range(tot_images/batch_size):
			label_arr_list = []
			for j in range(batch_size):
				temp = 	img_list[i*batch_size+j].split()
				img_path = temp[0]
				label = int(temp[1])
				if label == 0 :
					label = 1
				else:
					label = 0
				img = Image.open(img_path)
				if img is None:
					continue
				rsz_img = img.resize(img_size,Image.NEAREST)
				#rsz_ = np.asarray(rsz_img).reshape((1,img_size[0],img_size[1],3))
				imgs_arr[j] = rsz_img
				label_arr_list.append(label)

			#print(label_arr_list)
			label_arr = to_categorical(label_arr_list,num_classes=2)

			yield imgs_arr, label_arr
	
