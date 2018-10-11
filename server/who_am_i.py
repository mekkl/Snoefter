import socket

def get_my_ip():
  this_host = socket.gethostname()
  this_ip = socket.gethostbyname(this_host)
  return this_ip

if __name__ == '__main__':
  print(get_my_ip())
