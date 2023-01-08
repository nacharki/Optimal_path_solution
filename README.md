# Giskard technical test solution
Here is my solution to the odds technical test.

  The front-end is developed using HTML in index.html. It is created using jquery and ajax for minimal single-web-application creation
  
  The backend is developed using python. It contains:
  - The class Galaxy.py with two objects: Empire and Millennium Falcon, and all necessary methods to find feasible/acceptable/alternative/optimal paths and compute the odds of reaching Endor before the countdown. Note that Galaxy's methods require three librairies: pandas, networkx and sqlite3.
  - The executable give-me-the-odds.py, to be executed in the command-line interface (CLI).
  - The back-front connection webapp.py created using the library flask.
  
  
  The command-line interface can be executed in shell, for example1, as follows:
  $ python give-me-the-odds example1/millennium-falcon.json example1/empire.json


