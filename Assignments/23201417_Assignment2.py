from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time

# ===== Global Variables =====
WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900
BUTTON_SIZE = 44
OFFSET_TOP = 77
DIA_SIZE, DIA_ACCEL = 11, 20
C_LENGTH, C_HEIGHT, C_ACCEL = 222, 22, 22
INI_DIA_SPEED, INI_CAT_SPEED = 11, 111

dia_x, dia_y = random.randint(DIA_SIZE, WINDOW_WIDTH - DIA_SIZE), WINDOW_HEIGHT
dia_color = (
    random.uniform(0.25, 0.75),
    random.uniform(0.25, 0.75),
    random.uniform(0.25, 0.75),
)
dia_speed = INI_DIA_SPEED

cat_x = WINDOW_WIDTH // 2
cat_speed = INI_CAT_SPEED

paused = False
game_end = False
score = 0
cheating = False
last_time = 0
moving_left = False
moving_right = False


# ===== MPL ALGORITHM =====


def MPL(ix, iy, fx, fy):
    zone = find_zone(ix, iy, fx, fy)

    ix, iy = convert_to_zone0(ix, iy, zone)
    fx, fy = convert_to_zone0(fx, fy, zone)

    if ix > fx:  # Swap to make sure line drawing is done left to right
        ix, fx = fx, ix
        iy, fy = fy, iy

    dx, dy = fx - ix, fy - iy
    D = 2 * dy - dx
    inc_E, inc_NE = 2 * dy, 2 * (dy - dx)
    x, y = ix, iy
    while x <= fx:
        ox, oy = revert_to_original_zone(x, y, zone)
        glVertex2f(ox, oy)
        if D < 0:
            D += inc_E
        else:
            D += inc_NE
            y += 1
        x += 1


def find_zone(ix, iy, fx, fy):
    dx, dy = fx - ix, fy - iy
    if abs(dy) >= abs(dx):  # Closer to y-axis
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6
    else:  # Closer to x-axis
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7


def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def revert_to_original_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def check_collision():
    dia_right = dia_x + DIA_SIZE
    dia_left = dia_x - DIA_SIZE
    dia_top = dia_y + DIA_SIZE
    dia_bottom = dia_y - DIA_SIZE

    cat_right = cat_x + C_LENGTH // 2
    cat_left = cat_x - C_LENGTH // 2
    cat_top = C_HEIGHT
    cat_bottom = 1

    return (
        dia_right > cat_left
        and dia_left < cat_right
        and dia_top > cat_bottom
        and dia_bottom < cat_top
    )


def draw_line(ix, iy, fx, fy):
    MPL(ix, iy, fx, fy)


def draw_diamond(x, y, color, size):
    glColor3f(*color)
    MPL(x - size, y, x, y + size)  # left -> top
    MPL(x, y + size, x + size, y)  # top -> right
    MPL(x + size, y, x, y - size)  # right --> bottom
    MPL(x, y - size, x - size, y)  # bottom --> left


def draw_catcher(x, y, color, length, height):
    glColor3f(*color)
    hs = length // 2
    br = x + 3 * hs // 4
    bl = x - 3 * hs // 4
    MPL(bl, y, br, y)  # Bottom
    MPL(x + hs, y + height, x - hs, y + height)  # Top
    MPL(bl, y, x - hs, y + height)  # Left-curve
    MPL(br, y, x + hs, y + height)


def draw_arrow():
    glColor3f(0.0, 1.0, 0.77)
    x, y, s = OFFSET_TOP, WINDOW_HEIGHT - OFFSET_TOP, BUTTON_SIZE
    hs = s // 2  # half-size
    ots = s // 3  # onethird-size
    MPL(x - hs, y, x + hs, y)  # Horizontal Part
    MPL(x - hs, y, x, y + ots)  # Top Part
    MPL(x - hs, y, x, y - ots)  # Bottom Part


def draw_pause():
    glColor3f(1.0, 0.7, 0.0)
    x, y, s = WINDOW_WIDTH // 2, WINDOW_HEIGHT - OFFSET_TOP, BUTTON_SIZE
    hs = s // 2
    if not paused:
        MPL(x - hs, y - hs, x - hs, y + hs)
        MPL(x + hs, y - hs, x + hs, y + hs)
    else:
        MPL(x - hs, y - hs, x - hs, y + hs)
        MPL(x - hs, y - hs, x + hs, y)
        MPL(x - hs, y + hs, x + hs, y)


def draw_X():
    glColor3f(1.0, 0.0, 0.0)
    x, y, s = WINDOW_WIDTH - OFFSET_TOP, WINDOW_HEIGHT - OFFSET_TOP, BUTTON_SIZE
    hs = s // 2
    MPL(x - hs, y - hs, x + hs, y + hs)
    MPL(x - hs, y + hs, x + hs, y - hs)


def refresh_diamond():
    global dia_x, dia_y, dia_color
    if paused:
        return
    dia_x, dia_y = random.randint(DIA_SIZE, WINDOW_WIDTH - DIA_SIZE), WINDOW_HEIGHT
    dia_color = (
        random.uniform(0.25, 0.75),
        random.uniform(0.25, 0.75),
        random.uniform(0.25, 0.75),
    )


def restart_game():
    global score, paused, game_end, cat_x, dia_speed, cat_speed, INI_CAT_SPEED, INI_DIA_SPEED
    score = 0
    paused = False
    game_end = False
    cat_x = WINDOW_WIDTH // 2
    dia_speed = INI_DIA_SPEED
    cat_speed = INI_CAT_SPEED
    refresh_diamond()
    print("Starting Over")


def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    glPointSize(2.0)
    glBegin(GL_POINTS)

    if not game_end:
        draw_diamond(dia_x, dia_y, dia_color, DIA_SIZE)

    catcher_color = (1.0, 0.0, 0.0) if game_end else (1.0, 1.0, 1.0)
    draw_catcher(cat_x, 1, catcher_color, C_LENGTH, C_HEIGHT)
    draw_pause()
    draw_X()
    draw_arrow()

    glEnd()
    glutSwapBuffers()


def animate():
    global dia_y, dia_speed, last_time, cat_x, cat_speed, game_end, score

    current_time = time.perf_counter()
    delta_time = current_time - last_time if last_time else 0.02
    last_time = current_time

    if not game_end and not paused:
        dia_y -= dia_speed * delta_time
        dia_speed += DIA_ACCEL * delta_time
        if check_collision():
            score += 1
            print(f"Score: {score}")
            refresh_diamond()
        if dia_y + DIA_SIZE < 0:
            game_end = True
            print(f"Game Over! Final Score: {score}")
        if cheating:
            if cat_x > dia_x:
                cat_x = max(C_LENGTH // 2, cat_x - cat_speed * delta_time)
            else:
                cat_x = min(WINDOW_WIDTH - C_LENGTH // 2, cat_x + cat_speed * delta_time)
            cat_speed += C_ACCEL * delta_time
    if not game_end:
        if moving_left:
            cat_x = max(C_LENGTH // 2, cat_x - cat_speed * delta_time)
        if moving_right:
            cat_x = min(WINDOW_WIDTH - C_LENGTH // 2, cat_x + cat_speed * delta_time)
        cat_speed += C_ACCEL * delta_time

    glutPostRedisplay()


def special_key_listener(key, x, y):
    global moving_left, moving_right

    if paused or game_end or cheating:
        return

    if key == GLUT_KEY_LEFT:
        moving_left = True
        moving_right = False
    elif key == GLUT_KEY_RIGHT:
        moving_right = True
        moving_left = False


def key_up(key, x, y):
    global moving_left, moving_right

    if key == GLUT_KEY_LEFT:
        moving_left = False
    elif key == GLUT_KEY_RIGHT:
        moving_right = False


def mouse_listener(button, state, x, y):
    global paused
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return
    y = WINDOW_HEIGHT - y
    res_x, res_y, res_s = OFFSET_TOP, WINDOW_HEIGHT - OFFSET_TOP, BUTTON_SIZE
    if (x - res_x) ** 2 + (y - res_y) ** 2 <= res_s ** 2:
        restart_game()

    exit_x, exit_y, exit_s = (
        WINDOW_WIDTH - OFFSET_TOP,
        WINDOW_HEIGHT - OFFSET_TOP,
        BUTTON_SIZE,
    )
    if (x - exit_x) ** 2 + (y - exit_y) ** 2 <= exit_s**2:
        print(f"Goodbye! Final Score: {score}")
        glutLeaveMainLoop()

    pause_x, pause_y, pause_s = (
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT - OFFSET_TOP,
        BUTTON_SIZE,
    )
    if (x - pause_x) ** 2 + (y - pause_y) ** 2 <= pause_s**2:
        paused = not paused


def keyboard_listener(key, x, y):
    global cheating
    key = key.decode("utf-8")
    if key == "c" or key == "C":
        cheating = not cheating
        print(f"Cheat mode {'enabled' if cheating else 'disabled'}")


def main():

    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowPosition(150, 50)
    glutCreateWindow(
        b"G.M. Araf Mahfuz Rakib_23201417_CSE423_Assignment 2 - Diamond Catcher"
    )

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key_listener)
    glutSpecialUpFunc(key_up)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutMainLoop()


if __name__ == "__main__":
    main()
