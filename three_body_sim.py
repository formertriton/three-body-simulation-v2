"""
Enhanced Three-Body Problem Simulation Engine
High-performance gravitational physics with multiple integration methods
"""

import numpy as np
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class PhysicsSettings:
    """Configuration for physics simulation"""
    integration_method: str = "RK4"  # RK4, Leapfrog, Verlet, Euler
    adaptive_timestep: bool = True
    base_dt: float = 0.0005
    max_dt: float = 0.002
    min_dt: float = 0.0001
    collision_threshold: float = 0.05
    softening_parameter: float = 0.01
    energy_conservation_check: bool = True

class Particle:
    """Individual particle for trail effects"""
    def __init__(self, x: float, y: float, life: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = random.uniform(-0.1, 0.1)
        self.life = life
        self.max_life = life
        self.color = color
        self.size = random.uniform(1, 3)
    
    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        self.vx *= 0.98  # Friction
        self.vy *= 0.98

class Body:
    """Enhanced celestial body with particle effects and physics tracking"""
    
    def __init__(self, mass: float, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int] = (255, 255, 255), 
                 radius: float = 5, name: str = "Body"):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.name = name
        
        # Enhanced trail system
        self.trail = []
        self.max_trail_length = 1000
        self.trail_quality = 3  # Points per frame
        
        # Particle effects
        self.particles: List[Particle] = []
        self.particle_emission_rate = 2.0
        self.particle_timer = 0.0
        
        # Physics tracking
        self.force_x = 0.0
        self.force_y = 0.0
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0
        self.speed_history = []
        
        # Visual effects
        self.glow_intensity = 1.0
        self.pulsation_phase = random.uniform(0, 2 * math.pi)
        self.base_radius = radius
        
        # Collision detection
        self.collision_detected = False
        self.collision_timer = 0.0
    
    def add_to_trail(self, subdivisions: int = 1):
        """Add multiple points to trail for smoother curves"""
        if len(self.trail) > 0:
            last_x, last_y = self.trail[-1]
            for i in range(1, subdivisions + 1):
                t = i / subdivisions
                interp_x = last_x + (self.x - last_x) * t
                interp_y = last_y + (self.y - last_y) * t
                self.trail.append((interp_x, interp_y))
        else:
            self.trail.append((self.x, self.y))
        
        # Maintain trail length
        while len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def emit_particles(self, dt: float):
        """Emit trail particles"""
        self.particle_timer += dt
        
        if self.particle_timer >= 1.0 / self.particle_emission_rate:
            # Emit particle based on velocity
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed > 0.1:  # Only emit when moving
                particle_life = random.uniform(2.0, 4.0)
                particle = Particle(
                    self.x + random.uniform(-0.1, 0.1),
                    self.y + random.uniform(-0.1, 0.1),
                    particle_life,
                    self.color
                )
                self.particles.append(particle)
            self.particle_timer = 0.0
        
        # Update and remove dead particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update(dt)
    
    def update_visual_effects(self, dt: float):
        """Update visual effects like pulsation"""
        self.pulsation_phase += dt * 3.0
        pulse_factor = 1.0 + 0.1 * math.sin(self.pulsation_phase)
        self.radius = self.base_radius * pulse_factor
        
        # Update collision effects
        if self.collision_detected:
            self.collision_timer += dt
            if self.collision_timer > 1.0:
                self.collision_detected = False
                self.collision_timer = 0.0
    
    def get_position(self) -> np.ndarray:
        return np.array([self.x, self.y])
    
    def get_velocity(self) -> np.ndarray:
        return np.array([self.vx, self.vy])
    
    def set_state(self, x: float, y: float, vx: float, vy: float):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
    
    def get_kinetic_energy(self) -> float:
        return 0.5 * self.mass * (self.vx**2 + self.vy**2)
    
    def get_speed(self) -> float:
        return math.sqrt(self.vx**2 + self.vy**2)

class AdvancedThreeBodySimulation:
    """High-performance three-body simulation with multiple integration methods"""
    
    def __init__(self, settings: PhysicsSettings = None):
        self.settings = settings or PhysicsSettings()
        self.G = 1.0  # Gravitational constant
        self.bodies: List[Body] = []
        self.time = 0.0
        self.frame_count = 0
        self.paused = False
        
        # Performance tracking
        self.physics_time = 0.0
        self.render_time = 0.0
        self.fps_history = []
        
        # Energy and momentum conservation
        self.energy_history = []
        self.momentum_history = []
        self.angular_momentum_history = []
        
        # Adaptive timestep
        self.current_dt = self.settings.base_dt
        self.error_tolerance = 1e-8
        
        # Collision system
        self.collision_events = []
        
        # Center of mass tracking
        self.center_of_mass = np.array([0.0, 0.0])
        self.center_of_mass_velocity = np.array([0.0, 0.0])
    
    def add_body(self, body: Body):
        """Add a body to the simulation"""
        self.bodies.append(body)
        self.update_center_of_mass()
    
    def update_center_of_mass(self):
        """Calculate center of mass and velocity"""
        if not self.bodies:
            return
        
        total_mass = sum(body.mass for body in self.bodies)
        com_x = sum(body.mass * body.x for body in self.bodies) / total_mass
        com_y = sum(body.mass * body.y for body in self.bodies) / total_mass
        self.center_of_mass = np.array([com_x, com_y])
        
        com_vx = sum(body.mass * body.vx for body in self.bodies) / total_mass
        com_vy = sum(body.mass * body.vy for body in self.bodies) / total_mass
        self.center_of_mass_velocity = np.array([com_vx, com_vy])
    
    def calculate_gravitational_force(self, body1: Body, body2: Body) -> Tuple[float, float]:
        """Calculate gravitational force with softening parameter"""
        dx = body2.x - body1.x
        dy = body2.y - body1.y
        
        # Distance with softening
        r_squared = dx**2 + dy**2 + self.settings.softening_parameter**2
        r = math.sqrt(r_squared)
        
        # Check for collision
        actual_distance = math.sqrt(dx**2 + dy**2)
        if actual_distance < self.settings.collision_threshold:
            body1.collision_detected = True
            body2.collision_detected = True
            self.collision_events.append((self.time, body1.name, body2.name))
        
        # Gravitational force magnitude
        F_magnitude = self.G * body1.mass * body2.mass / r_squared
        
        # Force components
        Fx = F_magnitude * dx / r
        Fy = F_magnitude * dy / r
        
        return Fx, Fy
    
    def get_derivatives_rk4(self, state: np.ndarray) -> np.ndarray:
        """Calculate derivatives for RK4 integration"""
        derivatives = np.zeros_like(state)
        
        # Extract positions and velocities
        positions = []
        velocities = []
        masses = []
        
        for i in range(len(self.bodies)):
            idx = i * 4
            positions.append([state[idx], state[idx + 1]])
            velocities.append([state[idx + 2], state[idx + 3]])
            masses.append(self.bodies[i].mass)
        
        # Set velocity derivatives (dx/dt = vx, dy/dt = vy)
        for i in range(len(self.bodies)):
            idx = i * 4
            derivatives[idx] = state[idx + 2]      # dx/dt = vx
            derivatives[idx + 1] = state[idx + 3]  # dy/dt = vy
        
        # Calculate acceleration derivatives
        for i in range(len(self.bodies)):
            ax, ay = 0.0, 0.0
            
            for j in range(len(self.bodies)):
                if i != j:
                    dx = positions[j][0] - positions[i][0]
                    dy = positions[j][1] - positions[i][1]
                    
                    r_squared = dx**2 + dy**2 + self.settings.softening_parameter**2
                    r = math.sqrt(r_squared)
                    
                    # Acceleration due to body j
                    a_magnitude = self.G * masses[j] / r_squared
                    ax += a_magnitude * dx / r
                    ay += a_magnitude * dy / r
            
            # Store forces for visualization
            self.bodies[i].force_x = ax * self.bodies[i].mass
            self.bodies[i].force_y = ay * self.bodies[i].mass
            self.bodies[i].acceleration_x = ax
            self.bodies[i].acceleration_y = ay
            
            # Set acceleration derivatives
            idx = i * 4
            derivatives[idx + 2] = ax
            derivatives[idx + 3] = ay
        
        return derivatives
    
    def rk4_step(self, dt: float):
        """4th order Runge-Kutta integration step"""
        if len(self.bodies) < 2:
            return
        
        # Convert state to array
        state = np.zeros(len(self.bodies) * 4)
        for i, body in enumerate(self.bodies):
            idx = i * 4
            state[idx:idx+4] = [body.x, body.y, body.vx, body.vy]
        
        # RK4 integration
        k1 = self.get_derivatives_rk4(state)
        k2 = self.get_derivatives_rk4(state + 0.5 * dt * k1)
        k3 = self.get_derivatives_rk4(state + 0.5 * dt * k2)
        k4 = self.get_derivatives_rk4(state + dt * k3)
        
        new_state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        # Apply new state
        for i, body in enumerate(self.bodies):
            idx = i * 4
            body.set_state(new_state[idx], new_state[idx+1], 
                          new_state[idx+2], new_state[idx+3])
    
    def leapfrog_step(self, dt: float):
        """Leapfrog integration (symplectic, good for energy conservation)"""
        if len(self.bodies) < 2:
            return
        
        # Half velocity step
        for body in self.bodies:
            ax, ay = self.calculate_acceleration(body)
            body.vx += 0.5 * dt * ax
            body.vy += 0.5 * dt * ay
        
        # Full position step
        for body in self.bodies:
            body.x += dt * body.vx
            body.y += dt * body.vy
        
        # Half velocity step
        for body in self.bodies:
            ax, ay = self.calculate_acceleration(body)
            body.vx += 0.5 * dt * ax
            body.vy += 0.5 * dt * ay
    
    def calculate_acceleration(self, target_body: Body) -> Tuple[float, float]:
        """Calculate total acceleration on a body"""
        ax, ay = 0.0, 0.0
        
        for body in self.bodies:
            if body != target_body:
                dx = body.x - target_body.x
                dy = body.y - target_body.y
                
                r_squared = dx**2 + dy**2 + self.settings.softening_parameter**2
                r = math.sqrt(r_squared)
                
                a_magnitude = self.G * body.mass / r_squared
                ax += a_magnitude * dx / r
                ay += a_magnitude * dy / r
        
        return ax, ay
    
    def adaptive_timestep_control(self):
        """Adjust timestep based on system dynamics"""
        if not self.settings.adaptive_timestep:
            return
        
        # Calculate maximum acceleration
        max_acceleration = 0.0
        for body in self.bodies:
            acc_mag = math.sqrt(body.acceleration_x**2 + body.acceleration_y**2)
            max_acceleration = max(max_acceleration, acc_mag)
        
        # Adjust timestep based on acceleration
        if max_acceleration > 0:
            optimal_dt = math.sqrt(self.error_tolerance / max_acceleration)
            self.current_dt = np.clip(optimal_dt, 
                                    self.settings.min_dt, 
                                    self.settings.max_dt)
    
    def calculate_conserved_quantities(self):
        """Calculate energy, momentum, and angular momentum"""
        if len(self.bodies) < 2:
            return
        
        # Total energy
        kinetic_energy = sum(body.get_kinetic_energy() for body in self.bodies)
        potential_energy = 0.0
        
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                dx = self.bodies[j].x - self.bodies[i].x
                dy = self.bodies[j].y - self.bodies[i].y
                r = math.sqrt(dx**2 + dy**2)
                
                if r > self.settings.softening_parameter:
                    potential_energy -= (self.G * self.bodies[i].mass * 
                                       self.bodies[j].mass / r)
        
        total_energy = kinetic_energy + potential_energy
        
        # Total momentum
        total_momentum = np.array([0.0, 0.0])
        for body in self.bodies:
            total_momentum[0] += body.mass * body.vx
            total_momentum[1] += body.mass * body.vy
        
        # Total angular momentum
        total_angular_momentum = 0.0
        for body in self.bodies:
            # L = r × p = r × mv
            total_angular_momentum += (body.x * body.mass * body.vy - 
                                     body.y * body.mass * body.vx)
        
        # Store history
        self.energy_history.append(total_energy)
        self.momentum_history.append(np.linalg.norm(total_momentum))
        self.angular_momentum_history.append(abs(total_angular_momentum))
        
        # Limit history length
        max_history = 1000
        if len(self.energy_history) > max_history:
            self.energy_history.pop(0)
            self.momentum_history.pop(0)
            self.angular_momentum_history.pop(0)
    
    def step(self):
        """Advance simulation by one time step"""
        if self.paused:
            return
        
        # Choose integration method
        if self.settings.integration_method == "RK4":
            self.rk4_step(self.current_dt)
        elif self.settings.integration_method == "Leapfrog":
            self.leapfrog_step(self.current_dt)
        else:
            self.rk4_step(self.current_dt)  # Default fallback
        
        # Update visual effects and particles
        for body in self.bodies:
            body.add_to_trail(body.trail_quality)
            body.emit_particles(self.current_dt)
            body.update_visual_effects(self.current_dt)
            
            # Update speed history
            speed = body.get_speed()
            body.speed_history.append(speed)
            if len(body.speed_history) > 100:
                body.speed_history.pop(0)
        
        # Update system properties
        self.update_center_of_mass()
        self.adaptive_timestep_control()
        
        # Track conserved quantities
        if self.frame_count % 10 == 0:  # Every 10 frames
            self.calculate_conserved_quantities()
        
        self.time += self.current_dt
        self.frame_count += 1
    
    def reset(self):
        """Reset simulation state"""
        self.time = 0.0
        self.frame_count = 0
        self.current_dt = self.settings.base_dt
        self.energy_history = []
        self.momentum_history = []
        self.angular_momentum_history = []
        self.collision_events = []
        
        for body in self.bodies:
            body.trail = []
            body.particles = []
            body.speed_history = []
            body.collision_detected = False
    
    def toggle_pause(self):
        """Toggle simulation pause"""
        self.paused = not self.paused

# Enhanced scenario creation functions
def create_enhanced_figure_eight():
    """Enhanced figure-8 with better initial conditions and visual effects"""
    settings = PhysicsSettings(
        integration_method="RK4",
        base_dt=0.0008,
        adaptive_timestep=True
    )
    sim = AdvancedThreeBodySimulation(settings)
    
    # Precisely tuned figure-8 parameters
    body1 = Body(mass=1.0, x=-0.97000436, y=0.24208753, 
                vx=0.4662036850, vy=0.4323657300,
                color=(255, 80, 80), radius=6, name="Alpha")
    
    body2 = Body(mass=1.0, x=-0.97000436, y=-0.24208753,
                vx=0.4662036850, vy=-0.4323657300, 
                color=(80, 255, 80), radius=6, name="Beta")
    
    body3 = Body(mass=1.0, x=0.97000436, y=0.0,
                vx=-0.93240737, vy=0.0,
                color=(80, 80, 255), radius=6, name="Gamma")
    
    # Enhanced trail settings
    for body in [body1, body2, body3]:
        body.max_trail_length = 1500
        body.trail_quality = 2
        body.particle_emission_rate = 3.0
    
    sim.add_body(body1)
    sim.add_body(body2)
    sim.add_body(body3)
    
    return sim

def create_enhanced_solar_system():
    """Enhanced solar system with realistic mass ratios"""
    settings = PhysicsSettings(
        integration_method="Leapfrog",  # Better for planetary motion
        base_dt=0.001,
        adaptive_timestep=True
    )
    sim = AdvancedThreeBodySimulation(settings)
    sim.G = 10.0
    
    # Sun
    sun = Body(mass=333000, x=0.0, y=0.0, vx=0.0, vy=0.0,
              color=(255, 255, 100), radius=12, name="Sun")
    sun.particle_emission_rate = 5.0
    
    # Earth
    earth = Body(mass=1.0, x=4.0, y=0.0, vx=0.0, vy=3.2,
                color=(80, 150, 255), radius=4, name="Earth")
    
    # Moon
    moon = Body(mass=0.012, x=4.3, y=0.0, vx=0.0, vy=4.1,
               color=(200, 200, 200), radius=2, name="Moon")
    
    sim.add_body(sun)
    sim.add_body(earth)
    sim.add_body(moon)
    
    return sim

def create_binary_capture():
    """Binary star system with a captured planet"""
    settings = PhysicsSettings(
        integration_method="RK4",
        base_dt=0.0005,
        adaptive_timestep=True
    )
    sim = AdvancedThreeBodySimulation(settings)
    sim.G = 8.0
    
    # Binary stars
    star1 = Body(mass=50.0, x=-1.5, y=0.0, vx=0.0, vy=2.0,
                color=(255, 200, 100), radius=8, name="Star A")
    
    star2 = Body(mass=30.0, x=2.5, y=0.0, vx=0.0, vy=-3.3,
                color=(100, 200, 255), radius=6, name="Star B")
    
    # Captured planet
    planet = Body(mass=1.0, x=0.0, y=4.0, vx=1.8, vy=0.0,
                 color=(150, 255, 150), radius=3, name="Planet")
    
    for body in [star1, star2, planet]:
        body.max_trail_length = 2000
        body.particle_emission_rate = 2.0
    
    sim.add_body(star1)
    sim.add_body(star2)
    sim.add_body(planet)
    
    return sim