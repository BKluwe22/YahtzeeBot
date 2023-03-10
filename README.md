# A Pretty Strong Solitaire Yahtzee Bot with an Interactive Application

This repo contains a Yahtzee/Kniffel strategy implementation that scores an average of 
240.84767 and median of 241 over 1,000,000 simulated games.

You can play "against" the strategy in the practice application and simulate any 
number of legal actions from an arbitrary game state in accordance with the 
strategy.

## Installation

### Strategy Benchmark
Create a virtual environment, navigate to strategy-replication/ and run 
```
pip install -r requirements.txt
```

### Interactive Application
The easiest way to install and run this app through Docker Compose
```
cd YahtzeePracticeApp
docker compose build 
```

Alternatively, if you only want to play the game and not use the 
simulation dashboard, you can go into ```YahtzeePracticeApp/ui```, create a virtual 
environment, ```pip install -r requirements.txt```

## Usage

### Strategy Benchmark 
go into strategy-replication/ and run ```python main.py```

### Interactive Application
If you have built the images via Docker Compose, run ```docker compose up```
in the root of the YahtzeePracticeApp folder

If you have followed the alternative route, you can run ```python app.py```
in the ```YahtzeePracticeApp/ui``` folder

The ui is listening on port 9000 (http://127.0.0.1:9000). The simulation server is listening on port 5000 (http://127.0.0.1:5000)

