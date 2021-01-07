from datetime import datetime
from colorama import Fore, Back, Style, init

# Función para imprimir textos con estilos y datetime
def log_print(msg, style_code=None):
  current_datetime = datetime.now().replace(microsecond=0)

  if style_code is None:
    print('[' + str(current_datetime) + '] ' + msg)

  else:
    if style_code.lower() == 'success':
      print(Fore.GREEN + '[' + str(current_datetime) + '] ' + msg + Style.RESET_ALL)
    
    elif style_code.lower() == 'warning':
      print(Fore.YELLOW + '[' + str(current_datetime) + '] ' + msg + Style.RESET_ALL)
    
    elif style_code.lower() == 'error':
      print(Fore.RED + '[' + str(current_datetime) + '] ' + msg + Style.RESET_ALL)
    
    elif style_code.lower() == 'info':
      print(Fore.CYAN + '[' + str(current_datetime) + '] ' + msg + Style.RESET_ALL)