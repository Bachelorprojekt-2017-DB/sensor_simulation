# Rail2X Simulation DB Fernstrecke [![Build Status](https://travis-ci.org/Bachelorprojekt-2017-DB/sensor_simulation.svg?branch=master)](https://travis-ci.org/Bachelorprojekt-2017-DB/sensor_simulation) [![codecov](https://codecov.io/gh/Bachelorprojekt-2017-DB/sensor_simulation/branch/master/graph/badge.svg)](https://codecov.io/gh/Bachelorprojekt-2017-DB/sensor_simulation) [![Maintainability](https://api.codeclimate.com/v1/badges/deb26f5fde34ebf3ea08/maintainability)](https://codeclimate.com/github/Bachelorprojekt-2017-DB/sensor_simulation/maintainability)

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
