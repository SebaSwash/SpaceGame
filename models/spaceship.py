
class Spaceship:
  def __init__(self, position):
    self.x_pos = position[0]
    self.y_pos = position[1]
  
  def set_image_surface(self, image_surface):
    self.image_surface = image_surface
    # Se obtiene el rectángulo asociado a la superficie actual
    self.rect = self.image_surface.get_rect(center=(self.x_pos, self.y_pos))
  
  def draw(self, screen):
    self.rect = self.image_surface.get_rect(center=(self.x_pos, self.y_pos))
    screen.blit(self.image_surface, self.rect)