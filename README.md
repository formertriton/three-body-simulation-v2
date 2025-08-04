# \# Three Body Simulation


# This project simulates and animates the three-body gravitational problem using Python and Matplotlib.
Mathematical Background
The Three-Body Problem simulates the motion of three masses influenced by each other’s gravity.

Newton’s Law of Gravitation
The force exerted by body j on body i is:

F_ij = G * (m_i * m_j) / |r_j - r_i|^3 * (r_j - r_i)

where:

G is the gravitational constant

m_i and m_j are the masses

r_i and r_j are the position vectors of bodies i and j

|r_j - r_i| is the distance between bodies i and j

Equations of Motion
The acceleration of body i is:

d²r_i / dt² = (1 / m_i) * sum over j≠i of F_ij
which simplifies to:
d²r_i / dt² = G * sum over j≠i of m_j * (r_j - r_i) / |r_j - r_i|^3

This forms a set of coupled differential equations for the positions.

Numerical Integration
We rewrite the system using velocity v_i = dr_i/dt:

dr_i / dt = v_i

dv_i / dt = acceleration from gravitational forces

Using a time step Δt, update the velocities and positions as:

v_i(t + Δt) = v_i(t) + Δt * a_i(t)

r_i(t + Δt) = r_i(t) + Δt * v_i(t)

where a_i(t) is acceleration at time t calculated from the forces.

Initial Conditions
The simulation starts with initial positions r_i(0), velocities v_i(0), and masses m_i for all three bodies.

**SUMMARY**
The code implements:
Calculation of pairwise gravitational accelerations for each body.

Integration of positions and velocities forward in time using a numerical method.

Repeated frame updates for animation.

**UPCOMING**
# \- Includes animation saved as GIF.

# \- Demonstrates physics and numerical integration.



