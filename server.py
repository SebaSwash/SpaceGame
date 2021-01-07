import socket
import pickle
import threading
from colorama import init
from utils.log_print import log_print

init() # Inicialización para librería de colores

class Server:
  def __init__(self, host, port):
    try:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.bind((host, int(port)))
      self.sock.listen(5)
      self.connections = []

      log_print('Servidor inicializado correctamente con dirección ' + host + ':' + str(port) + '.', 'success')
      self.run()

    except Exception as error:
      log_print('Se ha producido el siguiente error al inicializar el servidor:', 'error')
      log_print(str(error), 'error')
  
  def connection_handler(self, connection, client_address):
    while True:
      try:
        data = connection.recv(4096)

        if not data:
          break

        # Se obtienen las coordenadas del paquete recibido
        player_coords = pickle.loads(data)
        data = pickle.dumps((client_address[1], player_coords))
        self.send_to_all(connection, data)

      
      except Exception as error:
        log_print('Se ha producido el siguiente error en la conexión con el cliente (' + str(client_address[0]) + ':' + str(client_address[1]) + ').', 'error')
        log_print(str(error), 'error')

        # Se remueve la conexión del cliente de la lista de conexiones
        self.connections.remove(connection)
        break
  
  # Método para enviar datos recibidos desde un cliente específico a los demás clientes conectados
  def send_to_all(self, from_connection, data):
    for connection in self.connections:
      if connection != from_connection:
        connection.send(data)


  def run(self):
    log_print('Servidor en ejecución.', 'success')
    while True:
      try:
        connection, client_address = self.sock.accept()
        self.connections.append(connection)

        log_print('Se ha establecido una nueva conexión con un cliente (' + str(client_address[0]) + ':' + str(client_address[1]) + ').', 'info')

        # Se genera un nuevo thread para atender al cliente conectado.
        client_thread = threading.Thread(target=self.connection_handler, args=(connection, client_address))
        client_thread.daemon = True
        client_thread.start()
      
      except KeyboardInterrupt:
        log_print('Servidor detenido manualmente.', 'warning')
        break


if __name__ == '__main__':
  server = Server('127.0.0.1', 3000)