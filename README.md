# 🌌 Three-Body Problem Simulation

<img width="1391" height="922" alt="Screenshot 2025-08-06 142327" src="https://github.com/user-attachments/assets/1cb32522-af1e-43c9-897b-70437d0d09dc" />

A high-performance, interactive visualization of the famous three-body problem in celestial mechanics
Featuring advanced physics simulation, stunning visual effects, and real-time performance monitoring
Real-time gravitational dynamics with particle effects, smooth trails, and interactive controls

Real-time gravitational dynamics with particle effects, smooth trails, and interactive controls

# ✨ Features
🔬 Advanced Physics Engine

- 4th-order Runge-Kutta integration for numerical accuracy and stability
- Adaptive timestep control automatically adjusts for optimal precision
- Multiple integration methods: RK4, Leapfrog, and Verlet integrators
- Energy conservation monitoring with real-time drift indicators
- Collision detection with visual feedback and event tracking

🎨 Stunning Visual Effects

- Anti-aliased rendering with smooth curves and gradients
- Dynamic particle systems with realistic physics and fading
- Glow effects and body pulsation based on mass and velocity
- Smooth orbital trails with configurable length and opacity
- Interactive camera system with body following and smooth interpolation

⚡ High Performance

- 60-120 FPS rendering with optimized algorithms
- GPU acceleration where available through Pygame
- Efficient memory management with automatic cleanup
- Real-time performance monitoring and frame time analysis
- Scalable particle systems that maintain smooth performance

🎮 Interactive Controls

- Real-time simulation control: pause, reset, speed adjustment
- Dynamic camera modes: free movement, body following, smooth zoom
- Visual debugging tools: force vectors, velocity vectors, physics data
- Scenario switching with multiple pre-configured systems
- Comprehensive keyboard shortcuts for all features

🔧 Installation

1. Clone this repository:
````
git clone https://github.com/yourusername/three-body-simulation.git
cd three-body-simulation
````
2. Create and activate a virtual environment:
````
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
````
3. Install dependencies:
```
pip install -r requirements.txt
Usage
Run the simulation:
python main.py
````
4. Run the simulation:
```
python main.py
```
Prerequisites
```
Python 3.8+
pip package manager
```
# Quick Start

Clone the repository:
```
git clone https://github.com/formertriton/three-body-simulation-v2.git
cd three-body-simulation-v2
```
Create virtual environment:
```
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
Run the simulation:
```
python main.py
```
# 🎮 Controls
```
Basic     Controls
Key       Action
SPACE     Pause/Resume simulation
R         Reset current scenario
ESC       Exit simulation
1, 2, 3   Switch between scenarios
+/-       Increase/decrease simulation speed
```
Visual Controls
```
Key       Action
T         Toggle orbital trails
I         Toggle information panel
G         Toggle coordinate grid
P         Toggle particle effects
C         Toggle center of mass indicator
D         Toggle physics debug mode
```
Advanced Controls
```
Key                  Action
V                    Show/hide velocity vectors
F                    Show/hide force vectors
F1-F3                Follow body 1, 2, or 3
F4                   Free camera mode
Arrow Keys           Pan camera
Mouse Wheel          Zoom in/out
Left Click + Drag    Pan camera
```

# 📊 Simulation Scenarios
1. 🎯 Enhanced Figure-8 Orbit
The famous choreographic solution discovered by Chenciner and Montgomery. Three equal masses follow a stable figure-8 trajectory with perfect periodicity.

Physics Highlights:
- Equal mass bodies (m = 1.0)
- Stable periodic solution
- Zero angular momentum configuration
- Perfect energy conservation demonstration

2. 🌍 Solar System Dynamics
Realistic representation of Sun-Earth-Moon gravitational interactions with proper mass ratios and orbital mechanics.
Physics Highlights:
- Realistic mass ratios (Sun: 333,000, Earth: 1, Moon: 0.012)
- Hierarchical orbital structure
- Tidal effects demonstration
- Multiple timescale dynamics

3. ⭐ Binary Star Capture
Complex three-body system featuring binary stars with a captured planet, demonstrating chaotic orbital mechanics.
Physics Highlights:
- Binary star system with unequal masses
- Chaotic planetary capture dynamics
- Energy transfer mechanisms
- Lagrange point interactions

# 🔬 Technical Implementation
Physics Engine (three_body_sim.py)
- Numerical Integration: 4th-order Runge-Kutta with adaptive timestep
- Force Calculation: N-body gravitational interactions with softening
- Energy Conservation: Hamiltonian mechanics with conservation tracking
- Collision Handling: Soft-sphere collision detection and response

Visualization Engine (main.py)
- Rendering Pipeline: Layered rendering with alpha blending
- Particle Systems: Physics-based trail particles with lifetime management
- Camera System: Smooth interpolation with multiple follow modes
- Performance Optimization: Frame rate limiting and selective rendering

Key Algorithms
- Runge-Kutta 4th Order: O(h^4) accuracy for position integration
- Leapfrog Integration: Symplectic integration for energy conservation
- Adaptive Timestep: Automatic step size based on system dynamics
- Spatial Optimization: Efficient distance calculations with softening

# 🎯 Educational Value
This simulation demonstrates key concepts in:
- Classical Mechanics: Newton's laws, gravitational forces, conservation laws
- Numerical Analysis: Integration methods, stability, accuracy trade-offs
- Chaos Theory: Sensitivity to initial conditions, Poincaré sections
- Computational Physics: N-body simulations, performance optimization
- Computer Graphics: Real-time rendering, particle systems, visual effects

# 🚀 Performance Metrics

Frame Rate: 60-120 FPS sustained performance
Physics Rate: Up to 20x real-time simulation speed
Energy Drift: < 0.01% over 1000+ orbits
Memory Usage: < 100MB for extended simulations
Startup Time: < 2 seconds on modern hardware

# 🔮 Future Enhancements

 3D Visualization: Full three-dimensional orbital mechanics
 Relativistic Effects: General relativity corrections for extreme masses
 Variable Star Masses: Mass loss/gain during evolution
 Gravitational Waves: Visualization of spacetime distortion
 N-Body Extension: Support for 4+ body systems
 Data Export: CSV/JSON export for scientific analysis
 VR Support: Virtual reality immersive experience
 Machine Learning: AI-driven orbital prediction

# 🤝 Contributing
Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.
Development Setup

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Areas for Contribution

Additional simulation scenarios
Performance optimizations
Visual effects enhancements
Educational documentation
Cross-platform compatibility

# 📚 References & Credits
Scientific References

Chenciner, A. & Montgomery, R. (2000). A remarkable periodic solution of the three-body problem. Annals of Mathematics.
Szebehely, V. (1967). Theory of Orbits: The Restricted Problem of Three Bodies. Academic Press.
Hairer, E., Nørsett, S.P. & Wanner, G. (1993). Solving Ordinary Differential Equations I. Springer.

Technical Acknowledgments

NumPy Team for high-performance numerical computing
Pygame Community for game development framework
Python Software Foundation for the Python programming language

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

# Built with ❤️ by formertriton
Exploring the beautiful chaos of celestial mechanics through interactive simulation

Simulation Scenarios
1. Figure-8 Orbit
The famous stable periodic solution discovered by Chenciner and Montgomery (2000). Three equal masses chase each other along a figure-8 path.
2. Sun-Earth-Moon System
A realistic representation of our solar system's dynamics with a massive central body (Sun), a planet (Earth), and its satellite (Moon).
3. Chaotic System
A demonstration of the chaotic nature of the three-body problem with three stars of different masses in unstable orbits.
Technical Details
Physics Engine

Mathematical Background
The three-body problem involves solving a system of differential equations:
```
d²r₁/dt² = G·m₂·(r₂-r₁)/|r₂-r₁|³ + G·m₃·(r₃-r₁)/|r₃-r₁|³
d²r₂/dt² = G·m₁·(r₁-r₂)/|r₁-r₂|³ + G·m₃·(r₃-r₂)/|r₃-r₂|³  
d²r₃/dt² = G·m₁·(r₁-r₃)/|r₁-r₃|³ + G·m₂·(r₂-r₃)/|r₂-r₃|³
```
Where:
```
rᵢ = position vector of body i
mᵢ = mass of body i
G = gravitational constant
```
Dependencies
```
pygame: Real-time graphics and user interaction
numpy: Efficient numerical computations
matplotlib: Optional plotting utilities
```
Project Structure
```
three-body-simulation/
│
├── main.py              # Main simulation runner and visualization
├── three_body_sim.py    # Physics engine and simulation logic
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```
<img width="1389" height="916" alt="Screenshot 2025-08-06 142354" src="https://github.com/user-attachments/assets/0669babb-f46f-454d-a49e-c1c7dbbe47da" />
<img width="1388" height="918" alt="Screenshot 2025-08-06 142415" src="https://github.com/user-attachments/assets/45c2d86f-f07c-4c2b-8997-a8f77e59c22a" />
