# Author : Vishal Popat Sale
import urllib.request
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import os
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()
API_Key = os.getenv("API_Key")

# assigning task (object-detection)
object_detector = pipeline("object-detection")

font = ImageFont.truetype("arial.ttf", 25)
# Function for drawing boxes on object
def draw_box(im, label, xmin, ymin, xmax, ymax, index, num_boxes):
	im_with_rectangle = ImageDraw.Draw(im)
	im_with_rectangle.rounded_rectangle((xmin, ymin, xmax, ymax), outline = "purple", width = 4, radius = 6)
	im_with_rectangle.text((xmin+35, ymin-25), label, fill="red", stroke_fill = "red", font = font)
	return im

# Open image
def open_image(image):
	bounding_boxes = object_detector(image)
	num_boxes = len(bounding_boxes)
	index = 0
	for bounding_box in bounding_boxes:
		box = bounding_box["box"]
		image = draw_box(image, bounding_box["label"], box["xmin"], box["ymin"], box["xmax"], box["ymax"], index, num_boxes)
		index += 1
	return image.show("image.png")

# This function is only used for extract the object name and show to user their count and name (Developed by Vishal Sale)
def object_name(image):
	objects = object_detector(image)
	object_all_names = []  #all objects names (dublicate values)
	object_name = []	   #individual
	object_count = []

	for object in objects:
		if object['label'] not in object_name:
			object_name.append(object['label'])
			object_all_names.append(object['label'])
		else:
			object_all_names.append(object['label'])

	for object in object_name:
		object_count.append(f"{object} : {object_all_names.count(object)}")
	print("-------------------------------------------------------------------------------------------------------------------------------------------------------")
	return f'detected object in {os.path.basename(image.filename)}:- [{", ".join(object_count)}]'

# This function for generating story/sentence based on object
client = OpenAI( api_key = API_Key )
def sentence_generation_using_openai(image):
	responce = client.chat.completions.create(
		model = 'gpt-3.5-turbo',
		messages = [
		{'role' : 'system', 'content' : f"Write a creative and short description of a scene depicted in an image in five lines. The image contains the following objects: {object_name}."},
		{'role' : 'user' , 'content' : f"{object_name(image)}"}
		],
		max_tokens=50,
		temperature = 0.4
	)
	print(f"Generated Sentence :-\n {responce.choices[0].message.content}")

# for combining the sentences and generating the story
def story():
	responce = client.chat.completions.create(
		model = 'gpt-3.5-turbo',
		messages = [
		{'role' : 'system', 'content' : f"Write a creative and short story based on the following combined scene descriptions: '{all_image_sentences}'. Story should be in a way such that the scenes comes together as one and combines story in a way that scenes relate each other. Complete story in 300 tokens"},
		{'role' : 'user' , 'content' : f"{all_image_sentences}"}
		],
		max_tokens=200,
		temperature = 0.4
	)
	print('\n')
	return f"Story :- {responce.choices[0].message.content}"

# Open image and show output
user_input = input("\n\n\nWhich image you want to pass for Story writing,\n1) internal image (local image)\n2) image URL\npress 1 or 2 : ")
# number_of_images = int(input("How many images you want to pass ? : "))
all_image_url = {}
all_image_sentences = {}

# getting images from user
i = 1
while i<=3:
	try:
		user_input = int(user_input)
		if user_input == 1 or user_input == 2:
			if user_input == 1:
				image_url = input(f"Enter Image {i} path or name : ")
				all_image_url[f"image_{i}"] = image_url
			else:
				image_url = input(f"Enter Image {i} url : ")
				all_image_url[f"image_{i}"] = image_url
		else:
			print("Invalid input, Please Enter 1 or 2")
			break
	except ValueError as err:
		print(err)
	i+=1

# generating sentence for each image
j = 1
while j<=3:
	if user_input == 1 or user_input == 2:
		if user_input == 1:
			with Image.open(all_image_url[f"image_{j}"]) as image:
				print(object_name(image))
				open_image(image)
				all_image_sentences[f"image_{j}"] = sentence_generation_using_openai(image)
		else:
			urllib.request.urlretrieve(all_image_url[f"image_{j}"], "image.png")
			with Image.open("image.png") as image:
				print(object_name(image))
				open_image(image)
				all_image_sentences[f"image_{j}"] = sentence_generation_using_openai(image)	
	else:
		break
	j+=1

print(story())