Three-Body Problem Simulation
An interactive, real-time visualization of the famous three-body problem in celestial mechanics, featuring accurate gravitational physics and multiple simulation scenarios.
Features

Accurate Physics: 4th-order Runge-Kutta integration for precise orbital mechanics
Multiple Scenarios: Figure-8 orbit, Sun-Earth-Moon system, and chaotic configurations
Interactive Controls: Real-time pause, speed control, zoom, and camera panning
Visual Effects: Orbital trails with fade effects and body glow rendering
Energy Conservation Tracking: Monitor numerical accuracy with energy drift indicators

Installation

Clone this repository:

bashgit clone https://github.com/yourusername/three-body-simulation.git
cd three-body-simulation

Create and activate a virtual environment:

bashpython -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies:

bashpip install -r requirements.txt
Usage
Run the simulation:
bashpython main.py
Controls
KeyActionSPACEPause/Resume simulationRReset current scenarioTToggle orbital trailsIToggle information panel1, 2, 3Switch between scenarios+/-Increase/decrease simulation speedMouse WheelZoom in/outLeft Click + DragPan camera
Simulation Scenarios
1. Figure-8 Orbit
The famous stable periodic solution discovered by Chenciner and Montgomery (2000). Three equal masses chase each other along a figure-8 path.
2. Sun-Earth-Moon System
A realistic representation of our solar system's dynamics with a massive central body (Sun), a planet (Earth), and its satellite (Moon).
3. Chaotic System
A demonstration of the chaotic nature of the three-body problem with three stars of different masses in unstable orbits.
Technical Details
Physics Engine

Integration Method: 4th-order Runge-Kutta (RK4) for high accuracy
Time Step: Adaptive stepping with collision detection
Coordinate System: Cartesian coordinates with center-of-mass frame
Energy Conservation: Monitored and displayed for numerical validation

Performance

Frame Rate: 60 FPS with real-time physics
Optimization: Efficient NumPy operations and selective rendering
Trail System: Configurable trail length with automatic cleanup

Mathematical Background
The three-body problem involves solving a system of differential equations:
d²r₁/dt² = G·m₂·(r₂-r₁)/|r₂-r₁|³ + G·m₃·(r₃-r₁)/|r₃-r₁|³
d²r₂/dt² = G·m₁·(r₁-r₂)/|r₁-r₂|³ + G·m₃·(r₃-r₂)/|r₃-r₂|³  
d²r₃/dt² = G·m₁·(r₁-r₃)/|r₁-r₃|³ + G·m₂·(r₂-r₃)/|r₂-r₃|³
Where:

rᵢ = position vector of body i
mᵢ = mass of body i
G = gravitational constant

Dependencies

pygame: Real-time graphics and user interaction
numpy: Efficient numerical computations
matplotlib: Optional plotting utilities

Project Structure
three-body-simulation/
│
├── main.py              # Main simulation runner and visualization
├── three_body_sim.py    # Physics engine and simulation logic
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
Contributing

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

Future Enhancements

 Add more initial condition presets
 Implement Poincaré sections for chaos analysis
 Add gravitational wave visualization
 Export simulation data to CSV
 3D visualization mode
 Multi-threaded physics computation

License
This project is licensed under the MIT License - see the LICENSE file for details.
References

Chenciner, A. & Montgomery, R. (2000). A remarkable periodic solution of the three-body problem in the case of equal masses. Annals of Mathematics, 152(3), 881-901.
Szebehely, V. (1967). Theory of Orbits: The Restricted Problem of Three Bodies. Academic Press.

Acknowledgments

NASA's Jet Propulsion Laboratory for orbital mechanics references
The NumPy and Pygame communities for excellent documentation
Historical contributions from Newton, Lagrange, and Poincaré to celestial mechanics