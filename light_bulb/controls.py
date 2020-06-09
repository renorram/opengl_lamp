from .camera import Camera
from pygame.constants import *


class Controls:
    key_map = {
        K_w: 'move_frontwards',
        K_s: 'move_backwards',
        K_d: 'move_right',
        K_a: 'move_left',

        K_UP: 'look_up',
        K_DOWN: 'look_down',
        K_RIGHT: 'look_right',
        K_LEFT: 'look_left',

        K_i: 'move_obj_up',
        K_k: 'move_obj_down',
        K_j: 'move_obj_left',
        K_l: 'move_obj_right',
        K_m: 'move_obj_frontwards',
        K_n: 'move_obj_backwards',
    }

    translate_vector = [0, 0, 0]

    def __init__(self, camera: Camera):
        self.camera = camera

    def handle_key(self, key):
        if key not in self.key_map:
            return

        func = self.__getattribute__(self.key_map[key])

        func()

    def move_frontwards(self):
        self.camera.eye_move_frontwards()

    def move_backwards(self):
        self.camera.eye_move_backwards()

    def move_right(self):
        self.camera.eye_move_right()

    def move_left(self):
        self.camera.eye_move_left()

    def look_up(self):
        self.camera.eye_look_up()

    def look_down(self):
        self.camera.eye_look_down()

    def look_right(self):
        self.camera.eye_look_right()

    def look_left(self):
        self.camera.eye_look_left()

    def orbital_control(self, button):
        if button == 4:
            self.camera.orbital_rotation()
        elif button == 5:
            self.camera.orbital_rotation(left=True)

    def move_obj_up(self):
        self.translate_vector[1] += .5

    def move_obj_down(self):
        self.translate_vector[1] -= .5

    def move_obj_left(self):
        self.translate_vector[0] -= .5

    def move_obj_right(self):
        self.translate_vector[0] += .5

    def move_obj_frontwards(self):
        self.translate_vector[2] += .5

    def move_obj_backwards(self):
        self.translate_vector[2] -= .5
