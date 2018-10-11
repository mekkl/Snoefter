# Snoefter
python package sniffer projekt

## Dependencies
[scapy](https://scapy.net/)

## Project structure
Snoefter/
├── client/
│   └── traffic_sim.py
├── server/
│   ├── simple_server.py
│   └── who_am_i.py
└── snoefter.py

### client/traffic_sim.py
Python script der skal imiterer en client der laver request op imod en server. Scriptet kan justeres ift. varighed for simulering (i sekunder), mængde af request pr. iteration og URL hvortil request skal laves.

Scriptet producerer en log fil `traffic_sim.log`.

Manual:

### server/simple_server.py
Python script der benyttes til at lave en simpel server, der kører på `http://localhost:5000`. Denne server kan benyttes til at lave request op imod fra client/traffic_sim.py.

Scriptet producerer en log fil `testserver.traffic.log`.

Manual:
