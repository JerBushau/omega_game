from math import atan2, pi, degrees
from pygame import mouse, draw, font, display


def angle_from_vec(vector):
    angle = atan2(vector.x, vector.y)
    angle %= 2 * pi
    return degrees(angle)


# handy functions from a tutorial needs re-write to better suit my needs
def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()


# create a button class rather than this function
def button(msg, x, y, width, height, colors, surface, action=None):
    """Function to easily create buttons"""

    m_pos = mouse.get_pos()
    click = mouse.get_pressed()

    if x + width > m_pos[0] > x and y + height > m_pos[1] > y:
        draw.rect(surface, colors[0], (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        draw.rect(surface, colors[1], (x, y, width, height))

    small_text = font.Font('freesansbold.ttf',20)
    text_surf, text_rect = text_objects(msg, small_text, colors[2])
    text_rect.center = ((x + (width/2)),(y + (height / 2)))
    surface.blit(text_surf, text_rect)
    display.update()
