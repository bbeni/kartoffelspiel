import pygame
from pygame.locals import *
from itertools import accumulate
import random

class AnimationSheet:
	def __init__(self, sprite_filename, cols, rows=1):
		self.durations = None

		self.sprite_filename = sprite_filename
		self.sheet = pygame.image.load(self.sprite_filename).convert_alpha()
		self.n_frames = rows*cols
		self.width = self.sheet.get_width() // cols
		self.height = self.sheet.get_height() // rows

		self.surfaces = []
		for row in range(rows):
			self.surfaces.append([])
			for col in range(cols):
				s = pygame.Surface((self.width, self.height)).convert_alpha()
				area = (col * self.width, row * self.height, self.width, self.height)
				s.blit(self.sheet, (0, 0), area=area)
				self.surfaces[row].append(s)

	def set_scale(self, factor):
		for row in range(len(self.surfaces)):
			for col in range(len(self.surfaces[row])):
				new_w = self.surfaces[row][col].get_width() * factor
				new_h = self.surfaces[row][col].get_height() * factor 
				self.surfaces[row][col] = pygame.transform.scale(self.surfaces[row][col], (new_w, new_h))

	def set_durations(self, row, durations):
		assert(row < len(self.surfaces))
		assert(len(durations) <= len(self.surfaces[0]))

		if self.durations is None:
			self.durations = [[1]*len(self.surfaces[0]) for _ in range(len(self.surfaces))]

		self.durations[row] = durations

	def frame(self, tick, row_index=0):
		if self.durations is None:
			row = self.surfaces[row_index]
			frame = row[tick % len(row)]
		else:
			dur = self.durations[row_index]
			tot_ticks = sum(dur)
			remainder = tick % tot_ticks
			end_times = accumulate(dur)
			for i, end in list(enumerate(end_times))[::-1]:
				if remainder - end >= 0:
					frame = self.surfaces[row_index][i+1]
					break
			else:
				frame = self.surfaces[row_index][0]
		return frame


if __name__ == "__main__":
	scale = 0.5
	display_surf = pygame.display.set_mode((512*1.5,512))
	animation = AnimationSheet('animation/kartoffel_sprite.png',9,2)
	animation.set_scale(scale)
	# 0 1 2 3 4 5 6 
	#   0 1 2     3
	animation.set_durations(row = 0, durations = [6, 1, 3, 2, 3, 1, 2, 1, 3])
	animation.set_durations(row = 1, durations = [20, 1])


	clock = pygame.time.Clock()
	FPS = 15
	tick = 0

	running = True

	jumping = False
	while running:
		for e in pygame.event.get():
		    if e.type == KEYDOWN:
		        if e.key == K_ESCAPE:
		            running = False
		        elif e.key == K_SPACE:
		        	jumping = not jumping
		        	jump_start_tick = tick


		display_surf.fill((0, 0, 0))

		if jumping:
			display_surf.blit(animation.frame(tick-jump_start_tick, 0), (0,0))
		else:
			display_surf.blit(animation.frame(random.randint(0, 1000), 1), (0,0))

		pygame.display.flip()
		clock.tick(FPS)
		tick += 1
