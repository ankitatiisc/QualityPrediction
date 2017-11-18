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


#Find which image is it box, layer or apple
#TO DO : Use enum
def id_entry(entry_keys):
	#print(entry_keys)
	if 'LayerID' in entry_keys:
		return 0,1,0
	elif 'ColorValue' in entry_keys:
		return 0,0,1
	else : 
		return 1,0,0


def gala_color_id(gala_color):
	if gala_color == 'full':
		return 0
	elif gala_color == 'medium':
		return 1
	elif gala_color == 'average':
		return 2

def gala_touch_id(gala_touch):
	if gala_touch == 'dent':
		return 0
	elif gala_touch == 'medium':
		return 1
	elif gala_touch == 'small':
		return 2
	elif gala_touch == 'NA':
		return 3

def gala_top_damage_id(gala_damage_type):
	if gala_damage_type == 'high':
		return 0
	elif gala_damage_type == 'medium':
		return 1
	elif gala_damage_type == 'low':
		return 2
	elif gala_damage_type == 'NA':
		return 3

def gala_spot_id(gala_spot_type):
	if gala_spot_type == 'high':
		return 0
	elif gala_spot_type == 'medium':
		return 1
	elif gala_spot_type == 'low':
		return 2
	elif gala_spot_type == 'NA':
		return 3
	
#Function for Gala
def get_gala_info(gala_data):
	color = [0,0,0]
	touches = [0,0,0,0]
	top_damages = [0,0,0,0]
	spot_marks = [0,0,0,0]
	for apple_data in gala_data:
		color_type = apple_data['ColorValue']
		type_id = gala_color_id(color_type)
		#print(type_id)
		color[type_id] += 1

		touches_type = apple_data['TouchesValue']
		type_id = gala_touch_id(touches_type)
		touches[type_id] += 1

		top_damage_type = apple_data['TopDamageValue']
		type_id = gala_top_damage_id(top_damage_type)
		top_damages[type_id] += 1

		spot_type = apple_data['SpotMarksValue']
		type_id = gala_spot_id(spot_type)
		spot_marks[type_id] += 1

	print('\nColor- Full:{}\tMedium:{}\tAverage:{}\n'.format(color[0],color[1],color[2]))
	print('Touches- Dent:{}\tMedium:{}\tSmall:{}\tNA:{}\n'.format(touches[0],touches[1],touches[2],touches[3]))
	print('Top Damage- High:{}\tMedium:{}\tLow:{}\tNA:{}\n'.format(top_damages[0],top_damages[1],top_damages[2],top_damages[3]))
	print('Spot- High:{}\tMedium:{}\tLow:{}\tNA:{}\n'.format(spot_marks[0],spot_marks[1],spot_marks[2],spot_marks[3]))
		

#process input data 
def process_apple_data(apple_data_list):
	count_gala = 0
	count_fuji = 0
	count_red_delicious = 0
	gala_data = []
	for apple_data in apple_data_list:
		apple_type = apple_data['ProductVariety']
		if apple_type == 'Gala':
			count_gala += 1
			gala_data.append(apple_data)
		elif apple_type == 'Fuji':
			count_fuji += 1
			#get_fuji_info()
		elif apple_type == 'RedDelicious':
			count_red_delicious += 1
			#get_red_delicious_info()
	print('Gala : {}\tFuji : {}\tRedDelicious : {}'.format(count_gala,count_fuji,count_red_delicious))
	get_gala_info(gala_data)
	
	 

#Add arguments here
parser = argparse.ArgumentParser()
parser.add_argument("-f","--file",help="JSON file path")
args = parser.parse_args()

#Check if path exists
if not os.path.exists(args.file):
	print('JSON file path doesnot exist')
	sys.exit()


count_boxes = 0
count_layers = 0
count_apples = 0
apple_data = []
#Read json-data
with open(args.file) as json_file:
	data = json.load(json_file)
	keys = data.keys()
	print('Length of keys in {}'.format(len(keys)))
	for k in keys:
		#print('key {} and member {}'.format(k,data[k]))
		b,l,a = id_entry(data[k].keys())
		count_boxes += b
		count_layers += l
		count_apples += a
		if a==1:
			apple_data.append(data[k])
			#process_apple_data(data[k])
			#print('key {} and member {}'.format(k,data[k]))
	print('box : {}\tlayers : {}\tapples : {}'.format(count_boxes,count_layers,count_apples))

	process_apple_data(apple_data)
	

