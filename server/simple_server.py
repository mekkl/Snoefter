from flask import Flask
import who_am_i
import logging

app = Flask(__name__)

@app.route("/")
def test():
  my_ip = who_am_i.get_my_ip()
  return f'Hello from test server! IP: {my_ip}'

if __name__ == '__main__':
  logging.basicConfig(filename='testserver.traffic.log', level=logging.INFO)
  app.run(host = "0.0.0.0")  # Listen to all requests.
