from kivy.config import Config
Config.set('graphics', 'width', '600') 
Config.set('graphics', 'height', '400')
Config.set('graphics', 'resizable', 'False')
Config.write()
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock

from random import choice
from cropper import ImageCropper

width = Window.size[0]
height = Window.size[1]

import sys, os
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

class Tile(Widget):
	radius = ListProperty()
	image = StringProperty()
	label = StringProperty()
	step = 0
	grid = None
	target = None
	direction = None
	x_tiles = []
	y_tiles = []

	def __init__(self, *args, **kwargs):
		self.radius = [4]
		super(Tile, self).__init__(*args, **kwargs)	
		#self.sound = SoundLoader.load(f"{path}/audio/click2.wav")	

	@property
	def position(self):
		return (int(self.x), int(self.y))

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			touch.grab(self)

	def on_touch_up(self, touch):
		if touch.grab_current is self:
			
			self.find_target_and_direction()
			if self.target:
				#self.sound.play()
				self.parent.moves += 1
				self.move_tiles()
				print(self.pos)
			touch.ungrab(self)

	def find_target_and_direction(self):
		
		self.x_tiles = list(filter(lambda tile: self.position[0] == tile.position[0], slide_puzzel.tile_list))
		self.y_tiles = list(filter(lambda tile: self.position[1] == tile.position[1], slide_puzzel.tile_list))

		grid_x = list(filter(lambda spot: self.position[0] == spot[0], self.grid))
		grid_y = list(filter(lambda spot: self.position[1] == spot[1], self.grid))

		def target_tile():
			target = None
			x_tiles_spots = [tile.position for tile in self.x_tiles]
			y_tiles_spots = [tile.position for tile in self.y_tiles]

			for grid_tile in grid_x:
				if grid_tile not in x_tiles_spots:
					target = grid_tile
					break

			for grid_tile in grid_y:
				if grid_tile not in y_tiles_spots:
					target = grid_tile	
					break
			return target	

		def find_direction():
			direction = ""
			if self.position[0] == self.target[0]:
				if self.position[1] < self.target[1]:
					direction = "up"
				else:
					direction = "down"
			if self.position[1] == self.target[1]:
				if self.position[0] < self.target[0]:
					direction = "right"
				else:
					direction = "left"
			return direction

		self.target = target_tile()
		try:
			self.direction = find_direction()
		except:
			pass

	def move_tiles(self):
		if len(self.x_tiles) < len(self.y_tiles) and self.direction == "up":
			#print("up direction")
			temp = list(filter(lambda tile: tile.position[1] < self.target[1] and tile.position[1] >= self.position[1], self.x_tiles))
			#print("length of temp:", len(temp))
			for tile in temp:
				tile.y += self.step

		if len(self.x_tiles) < len(self.y_tiles) and self.direction == "down":
			#print("down direction")
			temp = list(filter(lambda tile: tile.position[1] > self.target[1] and tile.position[1] <= self.position[1], self.x_tiles))
			#print("length of temp:", len(temp))
			for tile in temp:
				tile.y -= self.step

		if len(self.y_tiles) < len(self.x_tiles) and self.direction == "right":
			#print("right direction")
			temp = list(filter(lambda tile: tile.position[0] < self.target[0] and tile.position[0] >= self.position[0], self.y_tiles))
			#print("length of temp")
			for tile in temp:
				tile.x += self.step 

		if len(self.y_tiles) < len(self.x_tiles) and self.direction == "left":
			#print("left direction")
			temp = list(filter(lambda tile: tile.position[0] > self.target[0] and tile.position[0] <= self.position[0], self.y_tiles))
			#print("length of temp")
			for tile in temp:
				tile.x -= self.step 


class Main(Screen):
	background_image = StringProperty()
	grid = list()
	tile_step = 0
	arraged_rows = list()
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)
	
	def clear_current_data(self):
		del self.grid[:]
		self.tile_step = 0

	def create_grid(self, dimension):
		xp = width * .06
		yp = height * .07

		x = int(xp)
		y = int(yp)

		grid_size = width * .60
		self.tile_step = grid_size // dimension

		while len(self.grid) < (dimension ** 2):
			counter = 0
			while counter < dimension:
				self.grid.append((x, y))				
				x += self.tile_step
				counter += 1
			x = xp
			y += self.tile_step

		slide_puzzel.playground.board.size = (grid_size + 8, grid_size + 8)
		slide_puzzel.playground.board.pos = (xp - 6, yp - 6)
		self.add_tiles_to_grid(self.tile_step * .97)

	def add_tiles_to_grid(self, tile_size):
		for index, spot in enumerate(self.grid[1:]):
			tile = Tile(pos = spot, size = (tile_size, tile_size))
			#tile.label = str(len(self.grid) - index - 1)
			tile.step = self.tile_step
			tile.grid = self.grid
			slide_puzzel.playground.add_widget(tile)
			slide_puzzel.tile_list.append(tile)

		start = 0
		end = slide_puzzel.dimension
		grid = [spot for spot in self.grid[1:]]
		while len(self.arraged_rows) != slide_puzzel.dimension:
			self.arraged_rows.append(list(map(lambda x:x, grid[start:end])))
			start += slide_puzzel.dimension
			end += slide_puzzel.dimension
		self.arraged_rows = [list(reversed(row)) for row in self.arraged_rows]
		for spot in self.arraged_rows:
			print(spot)
			







class Playground(Screen):
	background_image = StringProperty()
	image = StringProperty()
	moves = NumericProperty(0)
	solution = dict()
	def __init__(self, *args, **kwargs):
		super(Playground, self).__init__(*args, **kwargs)

	def puzzel_solution(self):
		grid = [child.pos for child in self.children if isinstance(child, Tile)]
		solution = []
		index = 0
		while len(grid) < slide_puzzel.dimension:
			row = {}
			while len(row) < slide_puzzel.dimension:
				row.append(grid[index])
				index += 1
			self.solution.append(row)
		solution.reverse()

		tracker = slide_puzzel.dimension ** 2
		for i in solution:
			index = tracker - slide_puzzel.dimension
			for j in solution:
				self.solution[j] = index + 1
				index += 1
			tracker -= slide_puzzel.dimension
	

	def remove_tiles(self):
		children = [child for child in self.children if isinstance(child, Tile)]
		while len(children) > 0:self.remove_widget(children.pop(0))


	def add_puzzel_images(self):
		self.image = slide_puzzel.chosen_image
		crop_tool = ImageCropper(slide_puzzel.chosen_image, slide_puzzel.dimension*2)
		path = crop_tool.path

		skipped_index = slide_puzzel.dimension ** 2 - slide_puzzel.dimension
		children = [child for child in self.children if isinstance(child, Tile)]

		def sorted_images():
			for image in os.listdir(path):
				fn, ext = os.path.splitext(image)
				if fn != str(skipped_index + 1):
					yield image

		for tile, image in zip(children, sorted_images()):
			fn, ext = os.path.splitext(image)
			tile.image = resource_path(path + image)
			tile.label = fn
			#print(image)

	tracker = 0
	def shuffle_grid(self, dt):

		tile = choice(slide_puzzel.tile_list)
		tile.find_target_and_direction()
		if tile.target:
			tile.move_tiles()
		if self.tracker == 50:
			self.tracker = 0
			Clock.unschedule(self.shuffle_grid)
		self.tracker += 1

	def on_shuffle_call(self):
		#Clock.schedule_interval(self.shuffle_grid, .2)
		for cell in slide_puzzel.tile_list:
			print(cell.pos, cell.label)

	def on_volume_icon(self, inst):
		print(inst.icon)
		if inst.icon == "volume-high":
			inst.icon = "volume-off"
		else:
			inst.icon = "volume-high"


class ImageSelectionTiles(SmartTileWithLabel):
	def on_release(self):
		slide_puzzel.on_selected_image(self.source)



class ScrollableImages(MDGridLayout):
	def __init__(self, *args, **kwargs):
		super(ScrollableImages, self).__init__(*args, **kwargs)

		path = f"{slide_puzzel.path}/data/images/"
		for image_file in os.listdir(path):
			image_file = f"{path}{image_file}"
			tile = ImageSelectionTiles(source = image_file)
			tile.size_hint_y = None
			tile.height = "180dp"	
			self.add_widget(tile)	



class ImageSelection(Screen):
	def __init__(self, *args, **kwargs):
		super(ImageSelection, self).__init__(*args, **kwargs)
		pass

		
		
class SlidePuzzelGame(MDApp):
	grid_icon = ListProperty(['grid', 'grid', 'grid'])
	dimension = 4
	chosen_image = None
	path = os.path.abspath(".")
	tile_list = list()
	background_image = ""

	def on_selected_image(self, image):		
		self.chosen_image = image
		self.root.current = "main"

	def got_to_image_seletion(self, inst):
		self.root.current = "image_selection"

	def on_start(self):		
		self.main = self.root.get_screen('main')
		self.playground = self.root.get_screen('playground')
		self.main.background_image = self.background_image
		self.playground.background_image = self.background_image
		#self.playground.puzzel_solution()

		self.about_me = MDDialog(
				title = "dev/Mussab",
				text = "mussabblue@gmail.com",
				size_hint = (.4, .2))
		toast("Choose grid dimension and image")

	def callback(self, value):
		dimension = [4, 5, 6]
		for index, dim in enumerate(dimension):
			if value == dim:
				self.grid_icon[index] = 'checkbox-marked-circle-outline'
				self.dimension = dim
			else:
				self.grid_icon[index] = 'grid'


	# def on_play(self):
	# 	print("accessed....")
	# 	self.main.create_grid(self.dimension)
	# 	self.playground.add_puzzel_images()
	# 	self.root.current = "playground"

	def quit_session(self):
		for i in range(len(self.grid_icon)):
			self.grid_icon[i] = 'grid'
		self.dimension = None
		self.chosen_image = None
		self.main.clear_current_data()
		self.playground.remove_tiles()
		del self.tile_list[:]
		self.root.current = "main"


	init_counter = 0
	counter = 0
	def looper(self, dt):
		if self.dimension and self.chosen_image:
			self.main.create_grid(self.dimension)
			self.playground.add_puzzel_images()
			self.dimension = None
			self.chosen_image = None
			self.init_counter = 1
			toast("preparing ...", duration = 1.2)

		if self.counter >= 2:
			print("starting.......")
			self.counter = 0
			self.init_counter = 0
			self.root.current = "playground"
		self.counter += self.init_counter
				
	def build(self):
		self.theme_cls.primary_palette = "Teal"
		self.theme_cls.accent_palette = "Blue"
		self.background_image = choice(os.listdir(self.path+"/data/background"))
		self.background_image = f"{self.path}/data/background/{self.background_image}"
		Clock.schedule_interval(self.looper, 1)	
		return Builder.load_file("slide_puzzel.kv")

if __name__ in ('__main__'):
	slide_puzzel = SlidePuzzelGame()
	slide_puzzel.run()