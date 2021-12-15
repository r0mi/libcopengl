import logging
logg = logging.getLogger(__name__)
if __name__ == "__main__":
	logging.basicConfig(level=logging.NOTSET, format="%(asctime)s %(name)s %(levelname)-5s: %(message)s")

import sys
import time
import math
import random
import ctypes

from sdl2 import *

# uncomment these to use pyopengl
#from OpenGL.GL import *
#glTranslatef = glTranslate

from copengl import *


class FpsCounter:
	def __init__(self, update_interval_seconds=0.5):
		""" read self.fps for output """
		self.fps = 0.
		self.interval = update_interval_seconds
		self._counter = 0.
		self._age     = 0.
		self._last_output_age = 0.

	def tick(self, dt):
		self._age     += dt
		self._counter += 1.
		if self._age > self.interval:
			self.fps = self._counter / self._age
			self._age     = 0.
			self._counter = 0.


class Explosion:
	def __init__(self, x, y, direction, v):
		self.x, self.y = x, y
		self.direction = direction
		self.v = v
		self.age = 0.
		self.dead = False
		self.r = 0.
		self.lifetime = 0.6
		self.turndirection = direction

	def render(self):
		self.sideangle = 140.

		a = math.radians(self.direction + self.turndirection)
		x1, y1 = self.x + self.r * math.sin(a), self.y + self.r * math.cos(a)
		a = math.radians(self.direction + self.turndirection + self.sideangle)
		x2, y2 = self.x + self.r * math.sin(a), self.y + self.r * math.cos(a)
		a = math.radians(self.direction + self.turndirection - self.sideangle)
		x3, y3 = self.x + self.r * math.sin(a), self.y + self.r * math.cos(a)

		glColor4d(1., 0.3, 0.2, 1. - self.age / self.lifetime)

		glBegin(GL_TRIANGLE_FAN)
		glVertex3d(x1, y1, 0.)
		glVertex3d(x2, y2, 0.)
		glVertex3d(x3, y3, 0.)
		glEnd()

		glColor4d(0.4, 0., 0., 1. - self.age / self.lifetime)

		glBegin(GL_LINE_LOOP)
		glVertex3d(x1, y1, 0.)
		glVertex3d(x2, y2, 0.)
		glVertex3d(x3, y3, 0.)
		glEnd()

	def tick(self, dt):
		self.r += dt * 8.
		self.x += self.v * math.sin(math.radians(self.direction)) * dt
		self.y += self.v * math.cos(math.radians(self.direction)) * dt
		self.age += dt
		self.turndirection += dt * 1500.
		if self.age > self.lifetime:
			self.dead = True


class Bullet:
	def __init__(self, x, y, direction, v, owner):
		self.x, self.y = x, y
		self.direction = direction
		self.v = v
		self.age = 0.
		self.r = 0.5
		self.dead = False
		self.owner = owner

	def render(self):
		a = math.radians(self.direction)
		x2, y2 = self.x,  self.y
		x1, y1 = self.x + self.r * math.sin(a), self.y + self.r * math.cos(a)

		glShadeModel(GL_SMOOTH)

		glBegin(GL_LINES)
		glColor4d(0.3, 0.2, 0.1, 1.)
		glVertex3d(x1, y1, 0.)
		glColor4d(0.3, 0.2, 0.1, 0.)
		glVertex3d(x2, y2, 0.)
		glEnd()

	def tick(self, dt):
		self.x += self.v * math.sin(math.radians(self.direction)) * dt
		self.y += self.v * math.cos(math.radians(self.direction)) * dt
		self.age += dt
		if self.age > 3.:
			self.dead = True


class Crawly:
	def __init__(self, x, y):
		self.x,  self.y = x, y
		self.v = 0.
		self.acc = 0.
		self.direction = 0.
		self.leglen = 0.5*1.5
		self.legs = [[0., 0.] for i in range(10)]
		self.legs2 = [[0., 0.] for i in range(10)]
		self._place_legs()
		self._place_legs2()

		# feedback variables
		self.direction_new = 0.

		# 0 - default. red
		# 1 - friend. green
		# 2 - unknown. blue
		self.color = 0.
		self.speedlimit = 5.

		self.r = 0.3
		self.influence_radius = 1.0
		self.sideangle = 140.

		self.dead = False
		self.age = 0.

		self.randomstarttime = random.random() * 10.
		self.randomheartbeatspeed = (random.random() + 0.5) * 13.

	def _place_legs(self):
		side = -1.
		for i, l in enumerate(self.legs):
			side = -side
			if math.hypot(self.x - l[0], self.y - l[1]) > self.leglen + 0.1:
				# calc new leg position
				y = int(i / 2) + 1
				l[0] = self.x + math.sin(math.radians(self.direction - 8. * y * side)) * self.leglen
				l[1] = self.y + math.cos(math.radians(self.direction - 8. * y * side)) * self.leglen

	def _place_legs2(self):
		side = -1.
		for i, l2 in enumerate(self.legs2):
			# calc new leg position
			y = int(i / 2) + 1
			l = self.legs[i]
			l2[0] = self.x + (l[0] - self.x) / 2. + math.sin(math.radians(self.direction)) * self.leglen * .2
			l2[1] = self.y + (l[1] - self.y) / 2. + math.cos(math.radians(self.direction)) * self.leglen * .2

	def tick(self, dt):
		self.age += dt
		damping = 0.999
		self.direction = self.direction_new
		dx = math.sin(math.radians(self.direction))
		dy = math.cos(math.radians(self.direction))
		dv = self.acc * dt
		self.v += dv
		if self.v > self.speedlimit:
			self.v = self.speedlimit
		self.x += dx * (self.v * dt + self.acc * dt * dt / 2.)
		self.y += dy * (self.v * dt + self.acc * dt * dt / 2.)
		self.acc = 0

		self._place_legs()
		self._place_legs2()

	def _render_legs(self):
		glBegin(GL_LINES)
		glColor4d(0., 0., 0., 1.)

		# use simple legs
		#for l in self.legs:
		#    glVertex3d(self.x, self.y, 0.)
		#    glVertex3d(l[0], l[1], 0.)

		for l in self.legs2:
			glVertex3d(self.x, self.y, 0.)
			glVertex3d(l[0], l[1], 0.)

		for i, l in enumerate(self.legs):
			l2 = self.legs2[i]
			glVertex3d(l2[0], l2[1], 0.)
			glVertex3d(l[0], l[1], 0.)

		glEnd()

	def render(self):
		r = self.r + 0.05 * math.sin(self.age * self.randomheartbeatspeed + self.randomstarttime)

		a = math.radians(self.direction)
		x1, y1 = self.x + r * math.sin(a), self.y + r * math.cos(a)
		a = math.radians(self.direction + self.sideangle)
		x2, y2 = self.x + r * math.sin(a), self.y + r * math.cos(a)
		a = math.radians(self.direction - self.sideangle)
		x3, y3 = self.x + r * math.sin(a), self.y + r * math.cos(a)

		self._render_legs()

		if   self.color == 0: glColor4d(1., 0.3, 0.2, 1.)
		elif self.color == 1: glColor4d(0., 0.8, 0.2, 1.)
		elif self.color == 2: glColor4d(0., 0., 1., 1.)

		glBegin(GL_TRIANGLE_FAN)
		glVertex3d(x1, y1, 0.)
		glVertex3d(x2, y2, 0.)
		glVertex3d(x3, y3, 0.)
		glEnd()

		if self.color == 0: glColor4d(0.4, 0., 0., 1.)
		else: glColor4d(0., 0., 0., 1.)

		glBegin(GL_LINE_LOOP)
		glVertex3d(x1, y1, 0.)
		glVertex3d(x2, y2, 0.)
		glVertex3d(x3, y3, 0.)
		glEnd()

		# render the crawly influence area for debugging.
		if 0:
			glColor4d(0.7, 0.7, 0.7, 1.0)
			glBegin(GL_LINE_LOOP)
			for a in range(0, 360, 30):
				x, y = self.x + self.influence_radius * math.sin(math.radians(a)), self.y + self.influence_radius * math.cos(math.radians(a))
				glVertex(x, y, 0.)
			glEnd()


class Circle:
	def __init__(self, x, y, r, xxx_todo_changeme):
		(red, g, b, a) = xxx_todo_changeme
		self.x, self.y, self.r = x, y, r
		self.red, self.g, self.b, self.a = red, g, b, a

	def render(self):
		glColor4d(self.red, self.g, self.b, self.a)

		glBegin(GL_TRIANGLE_FAN)
		for a in range(0, 360, 10):
			x, y = self.x + self.r * math.sin(math.radians(a)), self.y + self.r * math.cos(math.radians(a))
			glVertex3f(x, y, 0.)
		glEnd()

		glBegin(GL_LINE_LOOP)
		for a in range(0, 360, 10):
			x, y = self.x + self.r * math.sin(math.radians(a)), self.y + self.r * math.cos(math.radians(a))
			glVertex3f(x, y, 0.)
		glEnd()


class CrawlyWorld:
	def __init__(self):
		self.crawlys = [self.new_crawly() for i in range(30)]
		self.crawlys[0].color = 1
		self.crawlys[0].speedlimit = 9.
		self.bullets = []
		self.explosions = []
		self.circles = []
		self.init_circles()

	def _set_projection(self, w, h, fov_x=90., z_near=1., z_far=50*1000.):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		#gluPerspective(fov_x * float(h) / w, float(w) / h, z_near, z_far)
		# make so that making the window larger will just bring more world to the view
		d = 0.04
		glOrtho(-w*d/2., w*d/2., -h*d/2., h*d/2., z_near, z_far)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def init_circles(self):
		self.circles.append(Circle(-3, 0, 2, (0.5, 0.5, 0.4, 1.)))
		self.circles.append(Circle(3, 1, 3, (0.5, 0.5, 1., 1.)))
		self.circles.append(Circle(-8, 7, 2.4, (0.7, 0.2, 1., 1.)))

	def new_crawly(self):
		c = Crawly(random.randrange(-1000., 1000.) * .01, random.randrange(-1000., 1000.) * .01)
		c.influence_radius = 2. - random.randrange(-10., 10.) * 0.01
		c.speedlimit = 5. + random.randrange(-10., 10.) * 0.2
		return c

	def crawly_angle(self, crawly1, crawly2):
		""" return angle between two creatures """
		a = math.degrees(math.atan2(crawly1.x - crawly2.x, crawly1.y - crawly2.y))
		offset, dummy = math.modf((a - crawly1.direction) / 360.)
		offset *= 360.
		if offset >  180.: offset -= 360.
		if offset < -180.: offset += 360.
		return offset

	def crawly_turn_direction(self, crawly1, crawly2):
		""" return in which direction the creature should turn in order to torn away from another """
		a = self.crawly_angle(crawly1, crawly2)
		if a < 0.: return 1.
		return -1.

	def tick(self, dt, keys):
		speed = 11.5
		turn_speed = 170.

		p = self.crawlys[0]

		if keys[SDL_SCANCODE_LEFT]:  p.direction_new -= turn_speed * dt
		if keys[SDL_SCANCODE_RIGHT]: p.direction_new += turn_speed * dt
		if keys[SDL_SCANCODE_UP]:    p.acc = speed * 0.6
		if keys[SDL_SCANCODE_DOWN]:  p.acc = -speed * 0.6

		bullet_speed = 6.
		if keys[SDL_SCANCODE_X]:
			self.bullets.append(Bullet(p.x, p.y, p.direction + 5 * (random.random() - 0.5), bullet_speed + p.v, p))

		# cleanup our object lists

		self.bullets    = [b for b in self.bullets if not b.dead]
		self.explosions = [e for e in self.explosions if not e.dead]
		self.crawlys    = [c for c in self.crawlys if not c.dead]

		# did bullets do any damage?
		# line-circle intersection. just test the bullet start/end points and crawly radius.

		for b in self.bullets:
			for c in self.crawlys:
				dist2 = (c.x - b.x) * (c.x - b.x) + (c.y - b.y) * (c.y - b.y)
				if dist2 < c.r * c.r and b.owner is not c and not c.dead:
					b.dead = True
					c.dead = True
					self.explosions.append(Explosion(c.x, c.y, c.direction, c.v))
					self.crawlys.append(self.new_crawly())

		bad_crawly_speed = 1.3
		bad_crawly_turn_speed = 180.

		# chase the player

		for c in self.crawlys:
			if c is not p:
				c.acc = bad_crawly_speed * 1.3
				c.direction_new += self.crawly_turn_direction(c, p) * bad_crawly_turn_speed * dt

		# avoid eachother
		# if distance if smaller than planned, then just steer away.

		if True:
			for c1 in self.crawlys:
				for c2 in self.crawlys:
					if c1 is not c2 and c1 is not p and c2:
						dist2 = (c1.x - c2.x) * (c1.x - c2.x) + (c1.y - c2.y) * (c1.y - c2.y)
						if dist2 < c1.influence_radius * c1.influence_radius:
							a = self.crawly_angle(c2, c1)
							if a > -90. and a < -90.: c1.v *= 0.9
							d = 1. - dist2 / (c1.influence_radius * c1.influence_radius)
							if a < 0.: c1.direction_new += bad_crawly_turn_speed * dt * 4. * d
							else:      c1.direction_new -= bad_crawly_turn_speed * dt * 4. * d

		# avoid the shapes

		if True:
			for c in self.crawlys:
				for circ in self.circles:
					dist = math.hypot(c.x - circ.x, c.y - circ.y)
					if dist < c.influence_radius * c.influence_radius:
						a = self.crawly_angle(c, circ)
						if a > -90. and a < -90.: c.v *= 0.9
						d = 1. - dist / (c.influence_radius * circ.r)
						if a < 0.: c.direction_new -= 2 * bad_crawly_turn_speed * dt * 4. * d
						else:      c.direction_new += 2 * bad_crawly_turn_speed * dt * 4. * d

		for c in self.crawlys:
			c.tick(dt)

		for b in self.bullets:
			b.tick(dt)

		for e in self.explosions:
			e.tick(dt)

	def render(self, window_w, window_h):
		glClearColor(0.8, 0.8, 1.8, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		#glColor(1,0,0,1)

		self._set_projection(window_w, window_h, 160)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslatef(0., 0., -15.)

		for c in self.circles:
			c.render()

		for c in self.crawlys:
			c.render()

		for b in self.bullets:
			b.render()

		for e in self.explosions:
			e.render()


class Main:
	def __init__(self):
		self.w = 800
		self.h = 600

		self.crawlyworld = CrawlyWorld()
		self.fpscounter = FpsCounter()
		self.fps_log_time = time.time()
		self.keys = None

	def run(self):
		if SDL_Init(SDL_INIT_VIDEO) != 0:
			logg.error(SDL_GetError())
			return -1

		window = SDL_CreateWindow(b"copengl example", SDL_WINDOWPOS_UNDEFINED,
								  SDL_WINDOWPOS_UNDEFINED, self.w, self.h,
								  SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)
		if not window:
			logg.error(SDL_GetError())
			return -1

		context = SDL_GL_CreateContext(window)

		glClearColor(0., 0., 0., 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		if SDL_GL_SetSwapInterval(-1): # 0 to disable vsync
			logg.error(SDL_GetError())
			if SDL_GL_SetSwapInterval(1):
				logg.error("SDL_GL_SetSwapInterval: %s", SDL_GetError())
				logg.error("vsync failed completely. will munch cpu for lunch.")

		self.keys = SDL_GetKeyboardState(None)
		self._init_gl()

		# init done. start the mainloop!

		last_t = time.time()

		event = SDL_Event()
		running = True
		while running:
			while SDL_PollEvent(ctypes.byref(event)) != 0:
				if event.type == SDL_QUIT:
					running = False

				if event.type == SDL_KEYDOWN:
					if event.key.keysym.scancode == SDL_SCANCODE_ESCAPE:
						running = False

				if event.type == SDL_WINDOWEVENT:
					if event.window.event == SDL_WINDOWEVENT_SIZE_CHANGED:
						self.w, self.h = event.window.data1, event.window.data2

			t = time.time()
			self._render_frame(t - last_t)
			last_t = t

			SDL_GL_SwapWindow(window)

		SDL_GL_DeleteContext(context)
		SDL_DestroyWindow(window)
		SDL_Quit()

	def _render_frame(self, dt):
		self.fpscounter.tick(dt)
		glViewport(0, 0, self.w, self.h)
		self.crawlyworld.tick(dt, self.keys)
		self.crawlyworld.render(self.w, self.h)

		t = time.time()
		if self.fps_log_time + 2 < t:
			logg.info("fps: %i", self.fpscounter.fps)
			self.fps_log_time = t

	def _init_gl(self):
		glDisable(GL_TEXTURE_2D)
		glDisable(GL_DEPTH_TEST)
		glDisable(GL_FOG)
		glDisable(GL_DITHER)
		glDisable(GL_LIGHTING)
		glShadeModel(GL_FLAT)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_LINE_SMOOTH)
		glDisable(GL_LINE_STIPPLE)


if __name__ == "__main__":
	logg.info("")
	logg.info("------------------------------------")
	logg.info("usage: press arrows and x")
	logg.info("------------------------------------")
	logg.info("")
	w = Main()
	sys.exit(w.run())
