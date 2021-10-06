
from PIL import Image
import os
class ImageCropper:

	areas = list()
	key = 0
	path = ""
	def __init__(self, image_file_path, grid_dimension):

		self.key = grid_dimension//2
		print(image_file_path)
		fn, ext = os.path.splitext(image_file_path)
		folder = f"{os.path.basename(fn)}/"
		puzzel_folder = f"{self.key}x{self.key}/"		

		self.path = os.path.abspath(os.getcwd())
		self.path = os.path.join(self.path, folder)	

		self.image = Image.open(image_file_path)
		self.image_size = self.image.size 
		
		self.width = self.image_size[0]// self.key
		self.height = self.image_size[1]// self.key


		if not os.path.exists(self.path):
			os.mkdir(self.path)

		self.path = os.path.join(self.path, puzzel_folder)

		if not os.path.exists(self.path):
			os.mkdir(self.path)
			self.area_to_crop()
			self.cropper()

	def area_to_crop(self):
		w = self.image_size[0] // self.key
		h = self.image_size[1] // self.key

		x = 0
		y = 0

		while self.height <= self.image_size[1]:
			while self.width <= self.image_size[0]:
				area = (x, y, self.width, self.height)
				self.areas.append(area)
				x += w
				self.width += w
			x = 0
			self.width = w
			y += h
			self.height += h

	def cropper(self):
		for index, area in enumerate(self.areas):
			image_name = str(index+1) 
			self.image.crop(area).save(f"{self.path}{image_name}.jpg")
		print("image cropper successfully")
		print("cropped images saved.")


# #image full path
# image = "img.jpg"
# path = os.path.abspath(os.getcwd())
# image_path = path + "/data/images/1.jpg"
# #grid dimension: 4 ----> 4x4
# grid = 8
# image_cropper = ImageCropper(image_path, grid)
# image_cropper.cropper()
