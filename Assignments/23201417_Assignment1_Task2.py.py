from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900
balls = []
frozen = False
blinking = False
flip = False
speed_factor = 1.0
blink_counter = 0

#Borders of Box
box_bottom = -400
box_top = 400
box_left = -750
box_right = 750

class Balls:
    vect = ((-1, 1), (-1, -1), (1, 1), (1, -1))
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx, self.dy = random.choice(self.vect)
        self.speed = random.uniform(0.05, 0.1)

        self.red = random.uniform(0.1, 1.0)
        self.green = random.uniform(0.1, 1.0)
        self.blue = random.uniform(0.1, 1.0)

    
    def draw_ball(self):
        global blink_counter, flip
        if blinking and blink_counter < 2222 and flip:
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(self.red, self.green, self.blue)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()
    def refresh(self):
        if not frozen:
            self.x += self.dx * self.speed * speed_factor
            self.y += self.dy * self.speed * speed_factor

            if self.x - 10 <= box_left or self.x + 10 >= box_right:
                self.dx *= -1
            
            if self.y - 10 <= box_bottom or self.y + 10 >= box_top:
                self.dy *= -1
            
        


def draw_box():
    glColor3f(0.7, 0.7, 0.7)
    glLineWidth(7.0)
    glBegin(GL_LINES)

    #Bottom
    glVertex2f(box_left, box_bottom)
    glVertex2f(box_right, box_bottom)
    #Top
    glVertex2f(box_left, box_top)
    glVertex2f(box_right, box_top)
    #Left
    glVertex2f(box_left + 4, box_bottom)
    glVertex2f(box_left + 4, box_top)
    #Right
    glVertex2f(box_right - 3, box_bottom)
    glVertex2f(box_right - 3, box_top)

    glEnd()


def convert_coordinate(x, y):
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b

    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setup_projection()
    draw_box()

    for b in balls:
        b.refresh()
        b.draw_ball()

    glutSwapBuffers()

def setup_projection():
    glPointSize(10.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-800, 800, -450, 450, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def animate():
    global blink_counter, flip
    if blinking:
        blink_counter += 1
        if blink_counter >= 2222:
            blink_counter = 0
            flip = not flip
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global speed_factor
    if not frozen:
        if key == GLUT_KEY_UP:
            speed_factor = min(5, speed_factor * 1.25)
        elif key == GLUT_KEY_DOWN:
            speed_factor = max(0.1, speed_factor * 0.8)

def mouse_listener(button, state, x, y):
    global blinking
    if state != GLUT_DOWN: return
    c_x, c_y = convert_coordinate(x, y)
    if button == GLUT_LEFT_BUTTON:
        blinking = not blinking
    elif button == GLUT_RIGHT_BUTTON:
        if box_left + 10 <= c_x <= box_right - 10 and box_bottom + 10 <= c_y <= box_top - 10:
            balls.append(Balls(c_x, c_y))

def keyboard_listener(key, x, y):
    global frozen
    if key == b" ":
        frozen = not frozen


def main():
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowPosition(150, 50)
    glutCreateWindow(b"G.M. Araf Mahfuz Rakib_23201417_CSE423_Assignment 1 - Amazing Box")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutMainLoop()


if __name__ == "__main__":
    main()
