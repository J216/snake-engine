
#execfile('/home/amber/gimp/snakec.py')

from math import sin, cos, radians
from random import randrange, choice
from time import sleep


class Engine:
    def __init__(self, location=[-1,-1], engine_type=-1):
        self.location = location
        if engine_type == -1:
            self.item_type = choice([0])
        else:
            self.item_type = engine_type

class Snake:
    def __init__(self, location=[-1,-1],name='Snake', snake_type=0):
        self.location = location
        self.plocation = location
        self.name = name
        self.engines_ate = 0
        self.heading = 0
        if snake_type == -1:
            self.item_type = choice([0,1])
        else:
            self.item_type = snake_type

    def turn(self, degrees=-1):
        if degrees == -1:
            degrees += choice([-45,-15,0,15,45])
        self.heading += degrees
        if self.heading > 360:
            self.heading -= 360
        if self.heading < 0:
            self.heading += 360

    def eat_engine(self, engines):
        for e in engines:
            if self.location == e.location:
                engines.remove(e)
                self.engines_ate += 1
                if self.item_type == 0:
                    self.item_type = 1


    def forward(self, blocked, width, height, engines):
        self.plocation = self.location
        self.location[0] += int(sin(radians(self.heading)))
        self.location[1] += int(cos(radians(self.heading)))
        if self.location[0] < 0:
            self.location[0] = 0
        if self.location[0] > width - 1:
            self.location[0] = width - 1
        if self.location[1] < 0:
            self.location[1] = 0
        if self.location[1] > height - 1:
            self.location[1] = height - 1
        if any(x.location == self.location for x in engines):
            self.eat_engine(engines)
            return 1
        return 0


class World:
    engines = []
    snakes=[]
    environ = []
    blocked = []
    def __init__(self,width=16,height=16):
        self.width = width
        self.height = height
        self.center = [width/2, height/2]

    def find_random_open(self):
        open_space = []
        while not open_space:
            open_space = [randrange(self.width-1),randrange(self.height-1)]
            if open_space in self.blocked:
                open_space = []
        return open_space

    def random_terra(self):
        return [choice([0,1,2,2,2,3,4]),choice([0,1,1,1])]

    def create_environ(self):
        environ=[]
        for y_row in range(self.height):
            environ_row = []
            for x_tile in range(self.width):
                environ_row.append(self.random_terra())
            environ.append(environ_row)
        self.environ = environ

    def add_engine(self, coord):
        e = Engine(coord)
        self.engines.append(e)
        self.blocked.append(e.location)

    def add_snake(self, coord, name):
        s = Snake(coord, name)
        self.snakes.append(s)
        
    def snake_on_engine(self):
        for s in self.snakes:
            for e in self.snakes:
                 if s.location == e.location:
                    return True
        return False



# image set up from gimp_be
def imageSetup(w=256, h=256,file_name=""):
    #Create new image from height and width
    if file_name == "":
	file_name='art.png'
    image = gimp.Image(w, h, RGB)
    gridSpacing = 32
    pdb.gimp_image_grid_set_spacing(image, gridSpacing, gridSpacing)
    pdb.gimp_image_grid_set_style(image, 1)
    new_layer = gimp.Layer(image, "Background", image.width, image.height, 0, 100, 0)
    pdb.gimp_image_add_layer(image, new_layer, 0)
    drawable = pdb.gimp_image_active_drawable(image)
    pdb.gimp_context_set_foreground((255, 255, 255))
    pdb.gimp_edit_bucket_fill_full(drawable, 0, 0, 100, 0, 1, 0, SELECT_CRITERION_COMPOSITE, 0, 0)
    pdb.gimp_context_set_foreground((0, 0, 0))
    pdb.gimp_context_set_background((255, 255, 255))
    gimp.Display(image)
    return image


# Close all - working but just guesses displays
def ca():
    try:
	for x in range(0, 500):
	    gimp.delete(gimp._id2display(x))
    except:
	print "close all failed"

def load_sprites(fn='/home/amber/gimp/snake_sprite.png'):
    global image
    if not pdb.gimp_image_get_layer_by_name(image, 'sprites'):
	    layer = pdb.gimp_file_load_layer(image, fn)
	    layer.name ='sprites'
	    pdb.gimp_image_add_layer(image, layer, 0)
	    pdb.gimp_item_set_visible(layer, 0)
	    return True
    else:
	    return False

def load_layer(layer_type='un-named!!!', opacity=100):
    global image
    if not pdb.gimp_image_get_layer_by_name(image, layer_type):
	    layer = pdb.gimp_layer_new(image, image.width, image.height, 1, layer_type, opacity, 0)
	    pdb.gimp_image_add_layer(image, layer, 0)
	    pdb.gimp_item_set_visible(layer, 1)
	    pdb.gimp_image_set_active_layer(image, layer)
	    pdb.gimp_selection_all(image)
	    drawable = pdb.gimp_image_active_drawable(image)
	    pdb.gimp_edit_clear(drawable)
	    return True
    else:
	    farmer_layer = pdb.gimp_image_get_layer_by_name(image, layer_type)
	    pdb.gimp_image_set_active_layer(image, farmer_layer)
	    pdb.gimp_selection_all(image)
	    drawable = pdb.gimp_image_active_drawable(image)
	    pdb.gimp_edit_clear(drawable)
	    return False

def paint_tile(loc,paint=[0,0],layer_type='environ'):
    global image
    sprite_layer = pdb.gimp_image_get_layer_by_name(image, "sprites")
    pdb.gimp_image_set_active_layer(image, sprite_layer)
    pdb.gimp_image_select_rectangle(image, 2, paint[0]*32, paint[1]*32, 32, 32)
    drawable = pdb.gimp_image_active_drawable(image)
    non_empty = pdb.gimp_edit_copy(drawable)
    paint_layer = pdb.gimp_image_get_layer_by_name(image, layer_type)
    pdb.gimp_image_set_active_layer(image, paint_layer)
    pdb.gimp_image_select_rectangle(image, 2, loc[0]*32, loc[1]*32, 32, 32)
    drawable = pdb.gimp_image_active_drawable(image)
    floating_sel = pdb.gimp_edit_paste(drawable, 1)
    pdb.gimp_floating_sel_anchor(floating_sel)
    pdb.gimp_selection_none(image)

def clear_tile(loc,layer_type='environ'):
    global image
    edit_layer = pdb.gimp_image_get_layer_by_name(image, layer_type)
    pdb.gimp_image_set_active_layer(image, edit_layer)
    pdb.gimp_image_select_rectangle(image, 2, loc[0]*32, loc[1]*32, 32, 32)
    drawable = pdb.gimp_image_active_drawable(image)
    pdb.gimp_edit_clear(drawable)
    pdb.gimp_selection_none(image)

def paint_environ(environ_in,blur=1):
    for y_row in range(len(environ_in)):
	    for x_pos in range(len(environ_in[0])):
	        paint_tile([x_pos, y_row], (environ_in[y_row][x_pos][0],environ_in[y_row][x_pos][1]))
    image = gimp.image_list()[0]
    if blur:
	    environ_layer = pdb.gimp_image_get_layer_by_name(image, "environ")
	    pdb.gimp_image_set_active_layer(image, environ_layer)
	    drawable = pdb.gimp_image_active_drawable(image)
	    pdb.plug_in_gauss(image, drawable, 30, 30, 0)

def paint_engines(engines):
    engine_types=[[0,3]]
    for e in engines:
	    paint_tile(e.location, engine_types[e.item_type], 'engines')

def paint_snakes(snakes):
    snake_types=[[1,2],[2,2]]
    for snake in snakes:
	    clear_tile(snake.plocation, 'snakes')
	    paint_tile(snake.location, snake_types[snake.item_type], 'snakes')


def paint_text(location=[10,10], size = 16, text="Default!@$#", clear=0, text_layer= 'hud', color=(255,0,0) ):
    global image
    hud_layer = pdb.gimp_image_get_layer_by_name(image, text_layer)
    pdb.gimp_image_set_active_layer(image, hud_layer)
    drawable = pdb.gimp_image_active_drawable(image)
    if clear:
        pdb.gimp_selection_all(image)
        pdb.gimp_edit_clear(drawable)
        pdb.gimp_selection_none(image)
    pdb.gimp_context_set_foreground(color)
    text_layer = pdb.gimp_text_fontname(image, drawable, location[0], location[1], text, 0, 0, size, 1, 'Sans Bold')
    pdb.gimp_floating_sel_anchor(text_layer)


def paint_hud(snakes=[]):
    score_row = 0
    for s in snakes:
        paint_text([10, score_row*24+10], 16, 'Snake'+str(score_row+1)+': '+str(s.engines_ate), score_row==0)
        score_row += 1

def make_animation(ms=250):
    global image
    global animation
    non_empty = pdb.gimp_edit_copy_visible(image)
    layer = pdb.gimp_layer_new(animation, image.width, image.height, 1, 'frame '+str(pdb.gimp_image_get_layers(animation)[0]+1)+'('+str(ms)+' ms)', 100, 0)
    pdb.gimp_image_add_layer(animation, layer, 0)
    pdb.gimp_item_set_visible(layer, 1)
    pdb.gimp_image_set_active_layer(animation, layer)
    drawable = pdb.gimp_image_active_drawable(animation)
    floating_sel = pdb.gimp_edit_paste(drawable, True)
    pdb.gimp_floating_sel_anchor(floating_sel)

def load_layers():
    load_sprites()
    load_layer('environ')
    load_layer('engines',90)
    load_layer('snakes')
    load_layer('hud',60)


##########################
## MAIN METHOD        ###
#########################

if __name__ == '__main__':
    game_score=0
    blur=1
    size=256
    engines=20
    snakes=6
    snake_moves=145
    snake_delay=0
    animate=1
    export_gif=1
    
    ca()
    if animate:
        animation = imageSetup(size,size)
    image = imageSetup(size,size)

    load_layers()
    
    
    w = World(image.width/32, image.height/32)
    w.create_environ()
    paint_environ(w.environ, blur)
    
    for i in range(engines):
        eng_loc = w.find_random_open()
        w.add_engine(eng_loc)

    paint_engines(w.engines)
    
    snake_pos = 0
    for i in range(snakes):
        w.add_snake([(w.width/2+snake_pos)-snakes/2,w.height/2],'Snake '+str(snake_pos+1))
        snake_pos += 1

    paint_snakes(w.snakes)

    while not len(w.engines) == 0:
        for s in w.snakes:
            clear_tile(s.location, 'snakes')
            game_score += s.forward(w.blocked, w.width, w.height, w.engines)
            s.turn( choice([-90,0,0,90,180]))
            paint_snakes([s])
            paint_hud(w.snakes)
            if w.snake_on_engine():
                clear_tile(s.location, 'engines')
                pdb.gimp_displays_flush()
            if animate:
                make_animation()
            sleep(snake_delay)
    if animate:
        make_animation()
    winner = w.snakes[0]
    for s in w.snakes:
        if s.engines_ate > winner.engines_ate:
            winner = s
            
    paint_text(location=[image.width/10,image.height/2], size=24, text=winner.name+" WINS!!!", clear=0, text_layer= 'hud', color=(0,255,255) )
    pdb.gimp_displays_flush()
    
    if animate:
                make_animation()
