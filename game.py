import pygame
import socket
import pickle
import threading
from colorama import init
from utils.log_print import log_print
from models.spaceship import Spaceship

init() # Inicialización para librería de colores
pygame.init() # Inicialización de Pygame

# Variables globales
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3000
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 120

class Game:
  def __init__(self, username):
    try:
      self.username = username
      self.score = 0

      self.game_init()

      # Socket para conexión con el servidor
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.connect((SERVER_HOST, SERVER_PORT))

      log_print('La conexión con el servidor ha sido establecida correctamente.')

      # Se genera un thread para obtener datos desde el servidor
      self.server_communication_thread = threading.Thread(target=self.server_communication_handler)
      self.server_communication_thread.daemon = True
      self.server_communication_thread.start()

      # Se inicia el proceso principal del juego
      self.run()
      exit()
      
    
    except Exception as error:
      log_print('Se ha producido el siguiente error al inicializar el juego y conectar con el servidor:', 'error')
      log_print(str(error), 'error')
  
  # Inicialización para Pygame
  def game_init(self):
    # Atributos para Pygame
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    self.clock = pygame.time.Clock()

    # Se genera la superficie de fondo
    self.bg_surface = pygame.image.load('./sprites/space-background.jpeg').convert()

    # Se genera el objeto del cohete
    self.spaceship = Spaceship((300,300))
    image_surface = pygame.image.load('./sprites/rocket.png').convert()

    image_surface = pygame.transform.scale(image_surface, (50, 50))
    self.spaceship.set_image_surface(image_surface)

    # Diccionario para almacenar las posiciones de los demás jugadores
    self.players_data = {}


  def draw_background(self):
    self.screen.blit(self.bg_surface, (0,0))
  
  def draw_players(self):
    for player_id in self.players_data.keys():
      x_pos, y_pos = self.players_data[player_id]
      spaceship = Spaceship((x_pos,y_pos))
      image_surface = pygame.image.load('./sprites/rocket-2.png').convert()
      image_surface = pygame.transform.scale(image_surface, (50, 50))
      spaceship.set_image_surface(image_surface)

      spaceship.draw(self.screen)
      

  def server_communication_handler(self):
    while True:
      try:
        data = self.sock.recv(4096)

        if not data:
          break

        # Se reciben las coordenadas de los demás jugadores, en caso de existir
        # y se almacenan en la lista
        player_data = pickle.loads(data)
        self.players_data[player_data[0]] = player_data[1]
        
      
      except Exception as error:
        log_print('Se ha producido el siguiente error en la conexión con el servidor:', 'error')
        log_print(str(error), 'error')
        break
  
  def run(self):
    while True:
      try:
        for event in pygame.event.get():

          if event.type == pygame.QUIT:
            # Se cierra el juego.
            pygame.quit()
            break

          # =========== Eventos de movimientos verticales de nave
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: # Movimiento vertical hacia arriba
              self.spaceship.y_pos -= 10
          
            if event.key == pygame.K_s: # Movimiento vertical hacia abajo
              self.spaceship.y_pos += 10
          
          # =========== Eventos de movimientos horizontales de nave
          if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: # Movimiento horizontal izquierdo
              self.spaceship.x_pos -= 10
          
            if event.key == pygame.K_d: # Movimiento horizontal derecho
              self.spaceship.x_pos += 10
          
        # Envío de datos al servidor mediante socket
        position = (self.spaceship.x_pos, self.spaceship.y_pos)
        data = pickle.dumps(position)
        self.sock.send(data)

        self.draw_background()
        self.spaceship.draw(self.screen)

        self.draw_players()

        pygame.display.update()
        self.clock.tick(FPS)

      except KeyboardInterrupt:
        log_print('Se ha interrumpido el juego manualmente.', 'error')
        break
    
    # Se cierra la conexión con el servidor
    self.sock.close()
    self.server_communication_thread.join()

if __name__ == '__main__':
  game = Game('S3B475')