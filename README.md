# Sensor network Simulation DB Fernstrecke

- Simulate Deutsche Bahn train network regarding decentralized sensor data exchange
- data from [db-fv-gtfs](https://github.com/fredlockheed/db-fv-gtfs)

Run:

- install [python3](https://www.python.org)
- install dependencies
  - ``pip3 install .``
- execute main ``python3 src/simulationMain.py``

Unit Testing:

- install coverage module (``pip3 install coverage``)
- to write a unit test, create a new file in the test folder named after following scheme: 'test_[module_name].py' (see unittest module for details)
- to run tests, run test_runner.py in root dir
- after running the tests, a coverage analysis can be found in htmlcov/index.html (``firefox htmlcov/index.html``)