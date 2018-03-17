import argparse
import json
import os
import sys

'''
Fuji:

ProductType = "Apple"
ProductVariety = {Fuji, Gala, RedDelicious}
ProductBrand
BrandPurchaseDate = DD-MM-YYYY
SampleLayerID = {Layer1, Layer2, Layer3, Layer4, Layer5}
ImageName = LayerID_timestamp.jpg
ImageDownloadUrl = "NA"
ColorValue = {Full, Medium, Average}
TouchesValue = {Dent, Medium, Small, NA}
RustingValue = {High, Medium, Low, NA}
ShapeValue = {Good, Medium, Average}
SpotMarksValue = {Yes, No, NA}

Gala:

ProductType = "Apple"
ProductVariety = {Fuji, Gala, RedDelicious}
ProductBrand
BrandPurchaseDate = DD-MM-YYYY
SampleLayerID = {Layer1, Layer2, Layer3, Layer4, Layer5}
ImageName = LayerID_timestamp.jpg
ImageDownloadUrl = "NA"
ColorValue = {Full, Medium, Average}
TouchesValue = {Dent, Medium, Small, NA}
TopDamageValue = {High, Medium, Low, NA}
SpotMarksValue = {Yes, No, NA}

RedDelicious:

ProductType = "Apple"
ProductVariety = {Fuji, Gala, RedDelicious}
ProductBrand
BrandPurchaseDate = DD-MM-YYYY
SampleLayerID = {Layer1, Layer2, Layer3, Layer4, Layer5}
ImageName = LayerID_timestamp.jpg
ImageDownloadUrl = "NA"
ColorValue = {Premium, ExtraFancy, Fancy, Half, Brown}
TouchesValue = {Dent, Medium, Small, NA}
TopDamageValue = {High, Medium, Low, NA}
SpotMarksValue = {Yes, No, NA}
PressureValue = {Good, Medium, Average}
BottomTouchesValue = {Large, Medium, Small, NA}
'''	 
def find(name,path):
	for root,dirs,files in os.walk(path):
		if name in files:
			return os.path.join(root,name)

def gala_color_id(gala_color):
	if gala_color == 'full':
		return 0
	elif gala_color == 'medium':
		return 1
	elif gala_color == 'average':
		return 2


imgs_path = '/home/papabaloo/Algro/data'
data_list = []
#json_file_paths = [ '/home/papabaloo/Algro/old/training-images-collection-nanda-export.json',
#		'/home/papabaloo/Algro/old/training-images-collection-santhosh-export.json',
#		'/home/papabaloo/Algro/new/training-images-collection-santhosh-export.json']

file_path = '/home/papabaloo/Algro/training-images-collection-export.json'#training-images-collection-export_full.json'
with open(file_path) as json_file:
	data = json.load(json_file)
	keys = data.keys()
	print('Length of keys in {}'.format(len(keys)))
	valid_keys_list = ['kashyap','santhosh','nanda','Version1_1']
	count = 0
	for k1 in keys:
		if k1 not in valid_keys_list:
			continue
		print(k1)
		data_ = data[k1] 
		if k1 == 'Version1_1':
			data_ = data[k1]['santhosh']
		for k in data_.keys():
			if 'ColorValue' in data_[k].keys():
				apple_type = data_[k]['ProductVariety']
				name = data_[k]['ImageName']
				imgs_path_ = imgs_path + '/PushPhotoData'
				if k1 == 'Version1_1':
					imgs_path_ = '/media/papabaloo/Data/algro_data'
				if apple_type == 'Gala':
					img_path = find(str(name),imgs_path)
					if img_path is None:
						print('token {} file {} not found'.format(k1,name))
						count += 1	
						continue
					#print(img_path)
					color_type = gala_color_id(data_[k]['ColorValue'])
					temp = img_path +" " + str(color_type)
					data_list.append(temp)

print('{} files not found'.format(count))	


f = open('img_list_color.txt','w')
for item in data_list:
	f.write("%s\n" %item)
f.close()

