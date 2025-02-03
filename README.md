# Optimal Path Solution with Risk Constraints 🚀

> A solution to the [Developer Technical Test](https://github.com/lioncowlionant/developer-test) demonstrating advanced path optimization with multiple constraints.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-green.svg)](https://streamlit.io/)
[![NetworkX](https://img.shields.io/badge/networkx-3.0+-orange.svg)](https://networkx.org/)

## 🎯 Problem Overview

This project implements a sophisticated path optimization solution that can be applied to various operations research scenarios. While themed around Star Wars (finding the optimal path for the Millennium Falcon), the underlying problem is a classic example of:

- **Path Optimization with Resource Constraints**
- **Risk-Aware Route Planning**
- **Time-Window Based Scheduling**
- **Multi-Objective Optimization**

### Similar Real-World Applications

This solution's approach can be adapted to solve various industry problems:

- **Supply Chain Optimization**
  - Delivery route planning with time windows
  - Fleet management with fuel constraints
  - Risk-aware transportation routing

- **Project Management**
  - Critical path analysis with resource constraints
  - Risk-based project scheduling
  - Multi-stage project planning

- **Network Design**
  - Telecommunication network routing
  - Utility grid optimization
  - Traffic flow optimization

## 🌟 Key Features

### Technical Implementation
- Graph-based path finding using NetworkX
- Resource-constrained path optimization
- Risk probability calculations
- Multi-objective optimization balancing:
  - Path length
  - Resource usage
  - Risk exposure
  - Time constraints

### Visualization & Analysis
- Interactive path visualization
- Risk probability assessment
- Resource utilization tracking
- Multiple path comparison

## 🛠️ Technical Stack

### Core Technologies
- **Python 3.8+**: Core implementation
- **NetworkX**: Graph algorithms and path optimization
- **Pandas**: Data manipulation and analysis
- **SQLite**: Route database management

### Interface Options
- **Streamlit**: Interactive web interface
- **CLI**: Command-line interface for automation
- **Python API**: For integration into other systems

## 🏗️ Architecture

### Core Components

#### Optimization Engine
```python
class PathOptimizer:
    def __init__(self):
        self.graph = None
        self.constraints = None
```

Key Features:
- Resource constraint handling
- Risk assessment
- Path feasibility checking
- Alternative path generation

## 🚀 Getting Started

### Prerequisites
```bash
pip install streamlit pandas networkx plotly
```

### Command Line Usage
```bash
python give-me-the-odds.py <config_file1.json> <config_file2.json>
```

### Web Interface
```bash
streamlit run app.py
```

## 📊 Implementation Examples

### Basic Path Finding
![Example Path](resources/example1.png)
- Demonstrates basic path optimization with single constraint

### Complex Routing
![Complex Route](resources/example2.png)
- Shows multi-constraint optimization with risk assessment

### Interactive Streamlit Interface
![Streamlit App](resources/Web_application.png)
- Shows the interactive web interface for path optimization

## 💡 Customization Possibilities

The solution can be adapted for various scenarios by modifying:

1. **Constraint Types**
   - Resource limitations
   - Time windows
   - Risk thresholds

2. **Optimization Objectives**
   - Minimize distance
   - Minimize risk
   - Balance multiple factors

3. **Risk Models**
   - Different probability distributions
   - Custom risk assessment functions
   - Multiple risk factors

## 📈 Performance

- Efficient graph-based implementation
- Handles complex constraints
- Scalable to large networks
- Real-time calculation capability

## 🤝 Contributing

Contributions are welcome! Areas of particular interest:

- Additional optimization algorithms
- New constraint types
- Performance improvements
- Real-world use case implementations

## 📚 Resources

- [Graph Theory in Python](link_to_resource)
- [Operations Research Basics](link_to_resource)
- [Path Optimization Techniques](link_to_resource)

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Development

- Extended optimization criteria
- Additional risk models
- Real-time path recalculation
- Machine learning integration

## ✨ Acknowledgments
- Original problem statement by [lioncowlionant].
- Inspiration from Star Wars universe.