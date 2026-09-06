from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900
rain_drops = []
incidence_angle = 0.0
sky_color = [0.1, 0.1, 0.2]
day_color = [0.1, 0.1, 0.2]
night_color = [0.3, 0.6, 0.9]

class Rain:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.uniform(10, 30)
        self.rain_speed = random.uniform(1.0, 2.0)
    def refresh_rain(self):
        self.x += math.sin(incidence_angle) * self.rain_speed
        self.y -= math.cos(incidence_angle) * self.rain_speed

        if self.x < -850:
            self.x = 850
        elif self.x > 850:
            self.x = -850
        if self.y < -450:
            self.y = random.uniform(500, 750)
            self.x = random.uniform(-850, 850)



def draw_sky():
    global sky_color
    glColor3f(*sky_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(-800, -200)
    glVertex2f(800, -200)
    glVertex2f(800, 450)
    glVertex2f(-800, -200)
    glVertex2f(-800, 450)
    glVertex2f(800, 450)
    glEnd()




def draw_house():
    #Walls
    glColor3f(0.7, 0.7, 0.7)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(-300, -200)
    glVertex2f(300, -200)
    glVertex2f(300, 100)
    glVertex2f(-300, -200)
    glVertex2f(300, 100)
    glVertex2f(-300, 100)
    glEnd()

    #Rooftop
    glColor3f(0.4, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-375, 100)
    glVertex2f(375, 100)
    glVertex2f(0, 300)
    glEnd()

    #Door
    glColor3f(0.3, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-70, -200)
    glVertex2f(70, -200)
    glVertex2f(70, 20)
    glVertex2f(-70, -200)
    glVertex2f(70, 20)
    glVertex2f(-70, 20)
    glEnd()

    #Windows
    glColor3f(0.4, 0.6, 0.7)
    glBegin(GL_TRIANGLES)
    #Left
    glVertex2f(-250,-50)
    glVertex2f(-150, -50)
    glVertex2f(-150, 50)
    glVertex2f(-250, -50)
    glVertex2f(-150, 50)
    glVertex2f(-250, 50)
    #Right
    glVertex2f(250,-50)
    glVertex2f(150, -50)
    glVertex2f(150, 50)
    glVertex2f(250, -50)
    glVertex2f(150, 50)
    glVertex2f(250, 50)
    glEnd()

    #Window Frame
    glColor3f(0.3, 0.2, 0.1)
    glLineWidth(4.0)
    glBegin(GL_LINES)
    #Left
    glVertex2f(-200, -50)
    glVertex2f(-200, 50)
    glVertex2f(-250, 0)
    glVertex2f(-150, 0)
    #Right
    glVertex2f(200, -50)
    glVertex2f(200, 50)
    glVertex2f(250, 0)
    glVertex2f(150, 0)
    glEnd()

    #Doorknob
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    #Left
    glVertex2f(40, -95)
    glVertex2f(50, -95)
    glVertex2f(50, -85)
    #Right
    glVertex2f(40, -95)
    glVertex2f(50, -85)
    glVertex2f(40, -85)
    glEnd()

    #Door Lines
    glColor3f(0.22, 0.11, 0.04)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(-40, -30)
    glVertex2f(40, -30)
    glVertex2f(-40, -160)
    glVertex2f(40, -160)
    glEnd()


def draw_ground():
    # Ground color
    glColor3f(0.0, 0.35, 0.15)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(-800, -450)
    glVertex2f(800, -450)
    glVertex2f(-800, -180)
    glVertex2f(-800, -180)
    glVertex2f(800, -180)
    glVertex2f(800, -450)
    glVertex2f(800, -450)

    glEnd()

def draw_grass():
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glColor3f(0.1, 0.7, 0.2)
    for i in range(-800, 800, 40):
        if -300 < i < 260: continue
        glVertex2f(i, -180)
        glVertex2f(i + 20, -150)
        glVertex2f(i + 40, -180)
    glEnd()

def draw_rain():
    glColor3f(0.5, 0.7, 0.9)
    glLineWidth(2.0)
    if not rain_drops:
        for i in range(250):
            x = random.uniform(-850, 850)
            y = random.uniform(-450, 450)
            rain_drops.append(Rain(x, y))

    glBegin(GL_LINES)                                                       

    for drop in rain_drops:                        
        dx = drop.size * math.sin(incidence_angle)
        dy = drop.size * math.cos(incidence_angle)
        glVertex2f(drop.x - dx, drop.y + dy)
        glVertex2f(drop.x + dx, drop.y - dy)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    draw_sky()
    draw_grass()
    draw_ground()
    draw_house()
    draw_rain()
    
    glutSwapBuffers()

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-800, 800, -450, 450, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def animate():
    for droplets in rain_drops:
        droplets.refresh_rain()
    glutPostRedisplay()


def special_key_listener(key, x, y):
    global incidence_angle
    p, q, r = day_color
    x, y, z = night_color
    if key == GLUT_KEY_UP:
        sky_color[0] = min(x, sky_color[0] + 0.01)
        sky_color[1] = min(y, sky_color[1] + 0.025)
        sky_color[2] = min(z, sky_color[2] + 0.035)
    elif key == GLUT_KEY_DOWN:
        sky_color[0] = max(p, sky_color[0] - 0.01)
        sky_color[1] = max(q, sky_color[1] - 0.025)
        sky_color[2] = max(r, sky_color[2] - 0.035)
    if key == GLUT_KEY_LEFT:
        incidence_angle -= 0.05
    elif key == GLUT_KEY_RIGHT:
        incidence_angle += 0.05
    incidence_angle = min(1, max(-1, incidence_angle))




def main():
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowPosition(150, 50)
    glutCreateWindow(b"G.M. Araf Mahfuz Rakib_23201417_CSE423_Assignment 1 - Rainfall")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutMainLoop()


if __name__ == "__main__":
    main()