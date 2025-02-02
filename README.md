# Millennium Falcon Calculator 

> This repository contains my solution to the [Developer Technical Test](https://github.com/lioncowlionant/developer-test) by lioncowlionant.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![jQuery](https://img.shields.io/badge/jquery-3.6+-yellow.svg)](https://jquery.com/)

A simple application to calculate the odds of the Millennium Falcon successfully reaching Endor and saving the galaxy. This solution implements both CLI and web interfaces for computing probabilities based on complex route calculations and Empire interceptor locations.

## 📋 Problem Statement

This project implements a solution for computing the probability of the Millennium Falcon reaching Endor before the Death Star destroys the planet. The calculation takes into account various factors including:

Route optimization with fuel constraints
Empire bounty hunter presence
Time-based countdown mechanics
Multiple possible paths and refueling strategies

- Route optimization with fuel constraints
- Empire bounty hunter presence
- Time-based countdown mechanics
- Multiple possible paths and refueling strategies

## 🛠️ Technical Stack


### Backend
- Python 3.8+ for core logic
- Flask for web server implementation
- SQLite for route database
- Key libraries:
  - `pandas` for data manipulation
  - `networkx` for graph calculations
  - `sqlite3` for database interactions

## 🏗️ Architecture

### Core Components

#### Galaxy Class
The heart of the application, implementing core game logic:

```python
class Galaxy:
    def __init__(self):
        self.empire = None
        self.millennium_falcon = None
```

Key Methods:
- `read_ROUTES()`: Database interaction for route retrieval
- `create_Graph()`: Graph construction from route data
- `find_feasible_paths()`: Path calculation within autonomy constraints
- `find_acceptable_paths()`: Direct path validation against countdown
- `find_alternative_paths()`: Alternative route calculation with delays
- `give_me_the_odds()`: Final probability computation with optimal path

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Flask framework
- Required Python packages:
  ```bash
  pip install pandas networkx flask
  ```

### Command Line Usage
```bash
python give-me-the-odds.py <millennium-falcon.json> <empire.json>
```

### Web Application Launch
```bash
flask --app webapp run
```
Access the application at `http://127.0.0.1:5000`

## 📊 Examples

### Example 1: Basic Route
![Example 1 Visualization](resources/example1.png)
Demonstrates basic path finding with minimal constraints.

### Example 2: Complex Routing
![Example 2 Visualization](resources/example2.png)
Shows multiple path options with interceptor consideration.

### Example 3: Delay Management
![Example 3 Visualization](resources/example3.png)
Illustrates route optimization with timing constraints.

### Example 4: Advanced Scenario
![Example 4 Visualization](resources/example4.png)
Demonstrates complex probability calculations with multiple variables.

## 🌐 Web Interface
![Web Application Interface](resources/Web_application.png)

The web interface provides an intuitive way to:
1. Upload Empire data files
2. Visualize potential routes
3. Calculate success probabilities
4. View detailed path analysis

## 🤝 Contributing
Contributions are welcome! Please feel free to reach out with any suggestions or improvements.

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Improvements
- Real-time route visualization
- Additional optimization algorithms
- Enhanced probability calculations
- Interactive route planning
- Performance optimizations for large datasets

## ✨ Acknowledgments
- Original problem statement by [lioncowlionant].
- Inspiration from Star Wars universe.