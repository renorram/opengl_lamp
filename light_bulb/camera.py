from OpenGL.GLU import gluLookAt
import math
import numpy as np


class Camera:
    rot_angle = 3.1415 / 2

    def __init__(self, eye: tuple, target: tuple, up: tuple):
        self.eye = np.array(eye, dtype=float)
        self.target = np.array(target, dtype=float)
        self.up = np.array(up, dtype=float)

        self.eye_target_rate = 2
        self.eye_move_rate = 0.5

    def set_look_at(self):
        gluLookAt(
            self.eye[0], self.eye[1], self.eye[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )

    def eye_look_up(self):
        self.target[1] = self.target[1] + self.eye_target_rate

    def eye_look_down(self):
        self.target[1] = self.target[1] - self.eye_target_rate

    def eye_look_right(self):
        self.target = self.move_target(True)

    def eye_look_left(self):
        self.target = self.move_target(False)

    def eye_move_frontwards(self):
        # self.eye[2] = self.eye[2] - self.eye_move_rate
        self.move_can(True)

    def eye_move_backwards(self):
        # self.eye[2] = self.eye[2] + self.eye_move_rate
        self.move_can(False)

    def eye_move_right(self):
        self.eye[0] += self.eye_move_rate
        self.target[0] += self.eye_move_rate

    def eye_move_left(self):
        self.eye[0] -= self.eye_move_rate
        self.target[0] -= self.eye_move_rate

    def orbital_rotation(self, left: bool = False):
        eye_dist = math.sqrt(sum([math.pow(cord, 2) for cord in self.eye]))
        # print(self.rot_angle)
        # print(self.eye)
        if left:
            self.rot_angle -= 0.02
            self.eye[2] = eye_dist * math.sin(self.rot_angle)
            self.eye[0] = eye_dist * math.cos(self.rot_angle)
        else:
            self.rot_angle += 0.02
            self.eye[2] = eye_dist * math.sin(self.rot_angle)
            self.eye[0] = eye_dist * math.cos(self.rot_angle)

    def move_can(self, ahead):
        delta = self.eye_move_rate
        p0 = self.eye
        p1 = self.target
        a = p1 - p0

        if ahead:
            signal = 1
        else:
            signal = -1
        p0 = p0 + delta * a * signal
        p1 = p1 + delta * a * signal

        # Câmera sobre o plano (X, Z)
        p0[1] = 0

        self.eye = p0
        self.target = p1

    def move_target(self, right):
        # translada a câmera para a origem
        t0 = self.target - self.eye

        # Ignora a componente Y
        t0[1] = 0

        # Calcula o raio do círculo
        r = math.sqrt(t0[0] * t0[0] + t0[2] * t0[2])

        # Calcula o seno e o cosseno e a tangente do ângulo que o vetor faz com o eixo X
        sin_alfa = t0[2] / r
        cos_alfa = t0[0] / r
        if cos_alfa == 0:
            if sin_alfa == 1:
                alfa = math.pi / 2
            else:
                alfa = - math.pi / 2
        else:
            tg_alfa = sin_alfa / cos_alfa

            # Calcula o arco cuja tangente é calculada no passo anterior
            alfa = np.arctan(tg_alfa)

            # Como o retorno de arctan varia somente entre -pi/2 e pi/2, testar o cosseno para
            # calcular o ângulo correto
            if cos_alfa < 0:
                alfa = alfa - math.pi

        if right:
            signal = 1
        else:
            signal = -1

        # Varia o ângulo do alvo (target)
        alfa = alfa + 0.1 * signal

        # Calcula o novo alvo (sobre o eixo Y)
        t0[0] = r * math.cos(alfa)
        t0[2] = r * math.sin(alfa)

        n_target = self.eye + t0

        return n_target
