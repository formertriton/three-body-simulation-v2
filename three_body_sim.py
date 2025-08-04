import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# Constants
G = 1.0  # Gravitational constant (scaled)

# Masses of the three bodies
masses = np.array([1.0, 1.0, 1.0])

# Initial positions and velocities (x, y, vx, vy) for 3 bodies
# Format: [x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3]
y0 = np.array([
    -1.0, 0.0,
    1.0, 0.0,
    0.0, 0.0,
    0.0, 0.3,
    0.0, -0.3,
    0.0, 0.0
])

def deriv(t, y):
    # Unpack positions and velocities
    r = y[:6].reshape(3, 2)
    v = y[6:].reshape(3, 2)
    
    a = np.zeros((3, 2))  # Accelerations
    
    # Calculate accelerations due to gravity
    for i in range(3):
        for j in range(3):
            if i != j:
                diff = r[j] - r[i]
                dist = np.linalg.norm(diff)
                a[i] += G * masses[j] * diff / dist**3
    
    dydt = np.concatenate([v.flatten(), a.flatten()])
    return dydt

# Time span and evaluation points
t_span = (0, 20)
t_eval = np.linspace(*t_span, 1000)

# Solve ODE
sol = solve_ivp(deriv, t_span, y0, t_eval=t_eval, rtol=1e-9)

# Set up plot
fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
lines = [ax.plot([], [], 'o')[0] for _ in range(3)]
trails = [ax.plot([], [], '-', alpha=0.5)[0] for _ in range(3)]

def init():
    for line, trail in zip(lines, trails):
        line.set_data([], [])
        trail.set_data([], [])
    return lines + trails

def update(frame):
    positions = sol.y[:6, frame].reshape(3, 2)
    
    for i, line in enumerate(lines):
        line.set_data([positions[i, 0]], [positions[i, 1]])
    
    # Plot trails for each body
    for i, trail in enumerate(trails):
        trail.set_data(sol.y[2*i, :frame], sol.y[2*i+1, :frame])
    
    return lines + trails

ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=20)

plt.title("Three-Body Problem Simulation")
plt.show()

ani = FuncAnimation(fig, update, frames=range(num_frames), interval=50)

# Save as mp4 (requires ffmpeg installed)
# ani.save('three_body_simulation.mp4', writer='ffmpeg', fps=30)

# Or save as gif (requires ImageMagick installed)
ani.save('three_body_simulation.gif', writer='imagemagick', fps=30)

plt.show()