import pygame
from entity import Entity

class Projectile:

  def __init__(self, img, pos, *groups):
    super().__init__(img, (500, 100, 120), pos, groups)
