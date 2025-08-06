"""
Enhanced Three-Body Simulation - Professional Grade Visualization
High-performance real-time physics with stunning visual effects
"""

import pygame
import pygame.gfxdraw
import sys
import math
import time
import numpy as np
from typing import List, Tuple, Optional
from three_body_sim import (
    AdvancedThreeBodySimulation, PhysicsSettings, Body,
    create_enhanced_figure_eight, create_enhanced_solar_system, 
    create_binary_capture
)

# Initialize Pygame with optimizations
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Enhanced constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
BACKGROUND_COLOR = (5, 5, 15)
UI_BACKGROUND = (20, 25, 35, 200)
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
YELLOW = (255, 255, 100)
ORANGE = (255, 150, 50)

class AdvancedRenderer:
    """High-performance rendering system with GPU acceleration where possible"""
    
    def __init__(self):
        # Display setup with hardware acceleration
        pygame.display.set_caption("Advanced Three-Body Simulation - Enhanced Edition")
        
        # Try hardware acceleration
        try:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 
                pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        except:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        
        # Enhanced fonts
        self.title_font = pygame.font.Font(None, 32)
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.tiny_font = pygame.font.Font(None, 14)
        
        # Simulation management
        self.current_sim = create_enhanced_figure_eight()
        self.simulation_speed = 2.0
        self.target_fps = 120  # Higher target FPS
        
        # Enhanced visual settings
        self.show_trails = True
        self.show_info = True
        self.show_physics_debug = False
        self.show_particles = True
        self.show_grid = True
        self.show_center_of_mass = True
        self.show_force_vectors = False
        self.show_velocity_vectors = False
        
        # Advanced camera system
        self.zoom = 60.0
        self.target_zoom = self.zoom
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.target_center_x = self.center_x
        self.target_center_y = self.center_y
        self.camera_follow_mode = 0  # 0: free, 1-3: follow bodies
        self.camera_smoothing = 0.95
        
        # Interactive controls
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.keys_pressed = set()
        
        # Performance monitoring
        self.frame_times = []
        self.physics_times = []
        self.render_times = []
        self.current_fps = 60.0
        
        # Visual effects
        self.background_stars = self.generate_background_stars()
        self.particle_systems = []
        
        # Scenarios
        self.scenarios = {
            "1": ("Enhanced Figure-8", create_enhanced_figure_eight),
            "2": ("Solar System", create_enhanced_solar_system),
            "3": ("Binary Capture", create_binary_capture)
        }
        self.current_scenario = "Enhanced Figure-8"
        
        # Sound effects (optional)
        self.sound_enabled = False
        try:
            # You can add sound files here
            pass
        except:
            pass
        
        # Create pre-computed glow surfaces for performance
        self.glow_surfaces = {}
        self.create_glow_surfaces()
    
    def generate_background_stars(self) -> List[Tuple[int, int, int]]:
        """Generate background star field"""
        stars = []
        for _ in range(200):
            x = np.random.randint(0, SCREEN_WIDTH)
            y = np.random.randint(0, SCREEN_HEIGHT)
            brightness = np.random.randint(50, 200)
            stars.append((x, y, brightness))
        return stars
    
    def create_glow_surfaces(self):
        """Pre-compute glow effects for better performance"""
        for radius in [5, 10, 15, 20, 25, 30]:
            surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            
            # Create radial gradient
            for r in range(radius * 2):
                alpha = max(0, 255 - int(255 * r / (radius * 2)))
                color = (255, 255, 255, alpha // 3)
                if alpha > 0:
                    pygame.gfxdraw.circle(surface, radius * 2, radius * 2, r, color)
            
            self.glow_surfaces[radius] = surface
    
    def world_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = int(self.center_x + x * self.zoom)
        screen_y = int(self.center_y - y * self.zoom)
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        world_x = (screen_x - self.center_x) / self.zoom
        world_y = -(screen_y - self.center_y) / self.zoom
        return world_x, world_y
    
    def update_camera(self):
        """Smooth camera movement and following"""
        # Camera following
        if self.camera_follow_mode > 0 and len(self.current_sim.bodies) >= self.camera_follow_mode:
            body = self.current_sim.bodies[self.camera_follow_mode - 1]
            target_x, target_y = self.world_to_screen(body.x, body.y)
            self.target_center_x = SCREEN_WIDTH // 2 - (target_x - SCREEN_WIDTH // 2)
            self.target_center_y = SCREEN_HEIGHT // 2 - (target_y - SCREEN_HEIGHT // 2)
        
        # Smooth interpolation
        self.center_x = self.center_x * self.camera_smoothing + self.target_center_x * (1 - self.camera_smoothing)
        self.center_y = self.center_y * self.camera_smoothing + self.target_center_y * (1 - self.camera_smoothing)
        self.zoom = self.zoom * 0.9 + self.target_zoom * 0.1
    
    def draw_background(self):
        """Draw animated background with stars"""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw moving stars
        if self.show_grid:
            for star_x, star_y, brightness in self.background_stars:
                # Make stars twinkle
                twinkle = math.sin(time.time() * 3 + star_x * 0.01) * 0.3 + 0.7
                color = (int(brightness * twinkle),) * 3
                pygame.draw.circle(self.screen, color, (star_x, star_y), 1)
        
        # Draw coordinate grid
        if self.show_grid:
            grid_spacing = max(20, int(50 * self.zoom / 60))
            for i in range(-10, 11):
                x_world = i * (1.0 / (self.zoom / 60))
                y_world = i * (1.0 / (self.zoom / 60))
                
                x_screen, _ = self.world_to_screen(x_world, 0)
                _, y_screen = self.world_to_screen(0, y_world)
                
                if 0 <= x_screen <= SCREEN_WIDTH:
                    pygame.draw.line(self.screen, (30, 30, 50), 
                                   (x_screen, 0), (x_screen, SCREEN_HEIGHT), 1)
                if 0 <= y_screen <= SCREEN_HEIGHT:
                    pygame.draw.line(self.screen, (30, 30, 50), 
                                   (0, y_screen), (SCREEN_WIDTH, y_screen), 1)
    
    def draw_enhanced_body(self, body: Body):
        """Draw body with advanced visual effects"""
        screen_x, screen_y = self.world_to_screen(body.x, body.y)
        
        # Skip if off-screen
        if not (-100 <= screen_x <= SCREEN_WIDTH + 100 and 
                -100 <= screen_y <= SCREEN_HEIGHT + 100):
            return
        
        # Dynamic radius based on zoom and mass
        display_radius = max(3, int(body.radius * (self.zoom / 60)))
        
        # Draw glow effect
        if body.collision_detected:
            glow_color = (255, 100, 100, 150)
        else:
            glow_color = (*body.color, 80)
        
        glow_radius = display_radius * 3
        if glow_radius in self.glow_surfaces:
            glow_surface = self.glow_surfaces[glow_radius].copy()
            glow_surface.fill(glow_color, special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(glow_surface, 
                           (screen_x - glow_radius * 2, screen_y - glow_radius * 2))
        
        # Draw main body with anti-aliasing
        pygame.gfxdraw.filled_circle(self.screen, screen_x, screen_y, 
                                   display_radius, body.color)
        pygame.gfxdraw.aacircle(self.screen, screen_x, screen_y, 
                               display_radius, WHITE)
        
        # Draw core highlight
        highlight_radius = max(1, display_radius // 3)
        highlight_color = tuple(min(255, c + 100) for c in body.color)
        pygame.gfxdraw.filled_circle(self.screen, 
                                   screen_x - highlight_radius//2, 
                                   screen_y - highlight_radius//2,
                                   highlight_radius, highlight_color)
        
        # Draw name and info
        if self.show_info and display_radius > 3:
            name_surface = self.small_font.render(body.name, True, WHITE)
            self.screen.blit(name_surface, 
                           (screen_x + display_radius + 5, screen_y - 8))
            
            # Show mass and speed
            if self.show_physics_debug:
                speed = body.get_speed()
                info_text = f"m:{body.mass:.1f} v:{speed:.2f}"
                info_surface = self.tiny_font.render(info_text, True, (200, 200, 200))
                self.screen.blit(info_surface, 
                               (screen_x + display_radius + 5, screen_y + 6))
    
    def draw_enhanced_trail(self, body: Body):
        """Draw smooth, fading trail with Bezier curves"""
        if not self.show_trails or len(body.trail) < 3:
            return
        
        # Convert trail to screen coordinates
        screen_trail = []
        for x, y in body.trail:
            sx, sy = self.world_to_screen(x, y)
            if -200 <= sx <= SCREEN_WIDTH + 200 and -200 <= sy <= SCREEN_HEIGHT + 200:
                screen_trail.append((sx, sy))
        
        if len(screen_trail) < 3:
            return
        
        # Draw trail segments with varying thickness and alpha
        num_points = len(screen_trail)
        for i in range(1, min(num_points, 500)):  # Limit for performance
            alpha = int(255 * (i / num_points) * 0.8)
            thickness = max(1, int(3 * (i / num_points)))
            
            # Create color with alpha
            color = (*body.color, alpha)
            
            # Draw anti-aliased line
            if alpha > 20:  # Skip very transparent segments
                start_pos = screen_trail[i-1]
                end_pos = screen_trail[i]
                
                # Create surface for alpha blending
                line_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(line_surface, color, start_pos, end_pos, thickness)
                self.screen.blit(line_surface, (0, 0))
    
    def draw_particles(self, body: Body):
        """Draw particle effects"""
        if not self.show_particles:
            return
        
        for particle in body.particles:
            screen_x, screen_y = self.world_to_screen(particle.x, particle.y)
            
            if 0 <= screen_x <= SCREEN_WIDTH and 0 <= screen_y <= SCREEN_HEIGHT:
                # Particle alpha based on remaining life
                alpha = int(255 * (particle.life / particle.max_life))
                color = (*particle.color, alpha)
                
                if alpha > 30:
                    size = max(1, int(particle.size * (self.zoom / 60)))
                    particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.gfxdraw.filled_circle(particle_surface, size, size, size, color)
                    self.screen.blit(particle_surface, (screen_x - size, screen_y - size))
    
    def draw_physics_vectors(self, body: Body):
        """Draw force and velocity vectors for physics debugging"""
        if not (self.show_force_vectors or self.show_velocity_vectors):
            return
        
        screen_x, screen_y = self.world_to_screen(body.x, body.y)
        
        # Velocity vector (green)
        if self.show_velocity_vectors:
            vel_scale = 20
            vel_end_x = screen_x + int(body.vx * vel_scale)
            vel_end_y = screen_y - int(body.vy * vel_scale)
            
            if math.sqrt(body.vx**2 + body.vy**2) > 0.1:
                pygame.draw.line(self.screen, GREEN, 
                               (screen_x, screen_y), (vel_end_x, vel_end_y), 2)
                # Arrow head
                angle = math.atan2(-body.vy, body.vx)
                arrow_length = 8
                arrow1_x = vel_end_x - arrow_length * math.cos(angle - 0.5)
                arrow1_y = vel_end_y + arrow_length * math.sin(angle - 0.5)
                arrow2_x = vel_end_x - arrow_length * math.cos(angle + 0.5)
                arrow2_y = vel_end_y + arrow_length * math.sin(angle + 0.5)
                
                pygame.draw.line(self.screen, GREEN, (vel_end_x, vel_end_y), 
                               (int(arrow1_x), int(arrow1_y)), 2)
                pygame.draw.line(self.screen, GREEN, (vel_end_x, vel_end_y), 
                               (int(arrow2_x), int(arrow2_y)), 2)
        
        # Force vector (red)
        if self.show_force_vectors:
            force_scale = 10
            force_end_x = screen_x + int(body.acceleration_x * force_scale)
            force_end_y = screen_y - int(body.acceleration_y * force_scale)
            
            if math.sqrt(body.acceleration_x**2 + body.acceleration_y**2) > 0.01:
                pygame.draw.line(self.screen, RED, 
                               (screen_x, screen_y), (force_end_x, force_end_y), 2)
    
    def draw_center_of_mass(self):
        """Draw center of mass indicator"""
        if not self.show_center_of_mass:
            return
        
        com_x, com_y = self.world_to_screen(
            self.current_sim.center_of_mass[0], 
            self.current_sim.center_of_mass[1]
        )
        
        if 0 <= com_x <= SCREEN_WIDTH and 0 <= com_y <= SCREEN_HEIGHT:
            # Draw crosshair
            pygame.draw.line(self.screen, YELLOW, 
                           (com_x - 10, com_y), (com_x + 10, com_y), 2)
            pygame.draw.line(self.screen, YELLOW, 
                           (com_x, com_y - 10), (com_x, com_y + 10), 2)
            pygame.draw.circle(self.screen, YELLOW, (com_x, com_y), 5, 2)
            
            # Label
            com_label = self.tiny_font.render("COM", True, YELLOW)
            self.screen.blit(com_label, (com_x + 15, com_y - 5))
    
    def draw_enhanced_ui(self):
        """Draw comprehensive user interface"""
        if not self.show_info:
            return
        
        # Main info panel
        panel_width = 350
        panel_height = 280
        panel_rect = pygame.Rect(10, 10, panel_width, panel_height)
        
        # Semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, UI_BACKGROUND, panel_surface.get_rect())
        pygame.draw.rect(panel_surface, WHITE, panel_surface.get_rect(), 2)
        self.screen.blit(panel_surface, panel_rect.topleft)
        
        # Title
        title_text = self.font.render(f"Three-Body Simulation", True, WHITE)
        self.screen.blit(title_text, (20, 20))
        
        # Simulation info
        y_offset = 50
        info_lines = [
            f"Scenario: {self.current_scenario}",
            f"Time: {self.current_sim.time:.3f}s",
            f"Timestep: {self.current_sim.current_dt:.6f}",
            f"Speed: {self.simulation_speed:.1f}x",
            f"FPS: {self.current_fps:.1f}",
            f"Zoom: {self.zoom:.1f}",
            f"Integration: {self.current_sim.settings.integration_method}",
            "",
            "Controls:",
            "SPACE - Pause/Resume", "R - Reset", "T - Toggle trails",
            "I - Toggle info", "G - Toggle grid", "P - Toggle particles",
            "F - Toggle force vectors", "V - Toggle velocity vectors",
            "C - Toggle center of mass", "D - Toggle debug mode",
            "1,2,3 - Switch scenarios", "+/- - Speed control",
            "Mouse wheel - Zoom", "Drag - Pan camera",
            "F1-F3 - Follow body", "F4 - Free camera"
        ]
        
        for line in info_lines:
            if line:
                if line.startswith("Controls:"):
                    text_surface = self.small_font.render(line, True, YELLOW)
                else:
                    text_surface = self.tiny_font.render(line, True, WHITE)
                self.screen.blit(text_surface, (20, y_offset))
            y_offset += 12
        
        # Performance panel
        if self.show_physics_debug:
            perf_panel = pygame.Rect(SCREEN_WIDTH - 250, 10, 240, 150)
            perf_surface = pygame.Surface((240, 150), pygame.SRCALPHA)
            pygame.draw.rect(perf_surface, UI_BACKGROUND, perf_surface.get_rect())
            pygame.draw.rect(perf_surface, GREEN, perf_surface.get_rect(), 2)
            self.screen.blit(perf_surface, perf_panel.topleft)
            
            perf_title = self.small_font.render("Performance", True, GREEN)
            self.screen.blit(perf_title, (SCREEN_WIDTH - 240, 20))
            
            # Performance metrics
            perf_y = 45
            avg_frame_time = sum(self.frame_times[-30:]) / max(len(self.frame_times[-30:]), 1)
            perf_lines = [
                f"Frame time: {avg_frame_time*1000:.1f}ms",
                f"Bodies: {len(self.current_sim.bodies)}",
                f"Particles: {sum(len(b.particles) for b in self.current_sim.bodies)}",
                f"Trail points: {sum(len(b.trail) for b in self.current_sim.bodies)}",
                f"Collisions: {len(self.current_sim.collision_events)}"
            ]
            
            for line in perf_lines:
                perf_surface = self.tiny_font.render(line, True, WHITE)
                self.screen.blit(perf_surface, (SCREEN_WIDTH - 240, perf_y))
                perf_y += 15
        
        # Energy conservation panel
        if len(self.current_sim.energy_history) > 1:
            energy_panel = pygame.Rect(SCREEN_WIDTH - 280, SCREEN_HEIGHT - 120, 270, 110)
            energy_surface = pygame.Surface((270, 110), pygame.SRCALPHA)
            pygame.draw.rect(energy_surface, UI_BACKGROUND, energy_surface.get_rect())
            
            initial_energy = self.current_sim.energy_history[0]
            current_energy = self.current_sim.energy_history[-1]
            energy_drift = abs((current_energy - initial_energy) / initial_energy) * 100 if initial_energy != 0 else 0
            
            # Color code energy conservation
            if energy_drift < 0.01:
                border_color = GREEN
            elif energy_drift < 0.1:
                border_color = YELLOW
            else:
                border_color = RED
            
            pygame.draw.rect(energy_surface, border_color, energy_surface.get_rect(), 2)
            self.screen.blit(energy_surface, energy_panel.topleft)
            
            energy_title = self.small_font.render("Conservation", True, border_color)
            self.screen.blit(energy_title, (SCREEN_WIDTH - 270, SCREEN_HEIGHT - 110))
            
            conservation_lines = [
                f"Energy drift: {energy_drift:.4f}%",
                f"Total energy: {current_energy:.6f}",
                f"Momentum: {self.current_sim.momentum_history[-1]:.6f}" if self.current_sim.momentum_history else "Momentum: N/A"
            ]
            
            cons_y = SCREEN_HEIGHT - 85
            for line in conservation_lines:
                cons_surface = self.tiny_font.render(line, True, WHITE)
                self.screen.blit(cons_surface, (SCREEN_WIDTH - 270, cons_y))
                cons_y += 15
        
        # Pause indicator
        if self.current_sim.paused:
            pause_text = self.title_font.render("⏸ PAUSED", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, 60))
            pause_bg = pygame.Rect(pause_rect.left - 10, pause_rect.top - 5, 
                                 pause_rect.width + 20, pause_rect.height + 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 200), pause_bg)
            pygame.draw.rect(self.screen, YELLOW, pause_bg, 2)
            self.screen.blit(pause_text, pause_rect)
    
    def handle_events(self) -> bool:
        """Enhanced event handling with more controls"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                if event.key == pygame.K_SPACE:
                    self.current_sim.toggle_pause()
                elif event.key == pygame.K_r:
                    self.reset_simulation()
                elif event.key == pygame.K_t:
                    self.show_trails = not self.show_trails
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_p:
                    self.show_particles = not self.show_particles
                elif event.key == pygame.K_c:
                    self.show_center_of_mass = not self.show_center_of_mass
                elif event.key == pygame.K_d:
                    self.show_physics_debug = not self.show_physics_debug
                elif event.key == pygame.K_f:
                    self.show_force_vectors = not self.show_force_vectors
                elif event.key == pygame.K_v:
                    self.show_velocity_vectors = not self.show_velocity_vectors
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.simulation_speed = min(self.simulation_speed * 1.2, 20.0)
                elif event.key == pygame.K_MINUS:
                    self.simulation_speed = max(self.simulation_speed / 1.2, 0.1)
                elif event.key == pygame.K_1:
                    self.switch_scenario("1")
                elif event.key == pygame.K_2:
                    self.switch_scenario("2")
                elif event.key == pygame.K_3:
                    self.switch_scenario("3")
                elif event.key == pygame.K_F1:
                    self.camera_follow_mode = 1
                elif event.key == pygame.K_F2:
                    self.camera_follow_mode = 2
                elif event.key == pygame.K_F3:
                    self.camera_follow_mode = 3
                elif event.key == pygame.K_F4:
                    self.camera_follow_mode = 0
            
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.dragging = True
                    self.last_mouse_pos = event.pos
                    self.camera_follow_mode = 0  # Disable following when dragging
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.target_center_x += dx
                    self.target_center_y += dy
                    self.last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.15 if event.y > 0 else 1/1.15
                self.target_zoom = np.clip(self.target_zoom * zoom_factor, 5, 500)
        
        # Handle continuous key presses
        if pygame.K_LEFT in self.keys_pressed:
            self.target_center_x += 5
        if pygame.K_RIGHT in self.keys_pressed:
            self.target_center_x -= 5
        if pygame.K_UP in self.keys_pressed:
            self.target_center_y += 5
        if pygame.K_DOWN in self.keys_pressed:
            self.target_center_y -= 5
        
        return True
    
    def switch_scenario(self, key: str):
        """Switch simulation scenario"""
        if key in self.scenarios:
            name, creator_func = self.scenarios[key]
            self.current_scenario = name
            self.current_sim = creator_func()
            self.reset_camera()
            print(f"Switched to: {name}")
    
    def reset_simulation(self):
        """Reset current simulation"""
        for key, (name, creator_func) in self.scenarios.items():
            if name == self.current_scenario:
                self.current_sim = creator_func()
                break
        self.reset_camera()
        print("Simulation reset")
    
    def reset_camera(self):
        """Reset camera to default position"""
        self.target_center_x = SCREEN_WIDTH // 2
        self.target_center_y = SCREEN_HEIGHT // 2
        self.target_zoom = 60.0
        self.camera_follow_mode = 0
    
    def update_simulation(self):
        """Update physics with performance monitoring"""
        start_time = time.time()
        
        # Multiple physics steps for higher simulation speed
        steps = max(1, int(self.simulation_speed))
        for _ in range(steps):
            self.current_sim.step()
        
        # Handle fractional speed
        fractional = self.simulation_speed - int(self.simulation_speed)
        if fractional > 0 and np.random.random() < fractional:
            self.current_sim.step()
        
        physics_time = time.time() - start_time
        self.physics_times.append(physics_time)
        if len(self.physics_times) > 60:
            self.physics_times.pop(0)
    
    def render_frame(self):
        """Render complete frame with all effects"""
        render_start = time.time()
        
        # Update camera
        self.update_camera()
        
        # Draw background
        self.draw_background()
        
        # Draw trails (behind bodies)
        if self.show_trails:
            for body in self.current_sim.bodies:
                self.draw_enhanced_trail(body)
        
        # Draw particles
        if self.show_particles:
            for body in self.current_sim.bodies:
                self.draw_particles(body)
        
        # Draw center of mass
        self.draw_center_of_mass()
        
        # Draw bodies
        for body in self.current_sim.bodies:
            self.draw_enhanced_body(body)
            self.draw_physics_vectors(body)
        
        # Draw UI
        self.draw_enhanced_ui()
        
        # Update display
        pygame.display.flip()
        
        render_time = time.time() - render_start
        self.render_times.append(render_time)
        if len(self.render_times) > 60:
            self.render_times.pop(0)
    
    def run(self):
        """Main enhanced simulation loop"""
        print("🚀 Enhanced Three-Body Simulation Started!")
        print("📋 Press I to toggle info panel, D for debug mode")
        print("🎮 Use F1-F3 to follow bodies, F4 for free camera")
        
        running = True
        frame_start_time = time.time()
        
        while running:
            current_time = time.time()
            
            # Handle events
            running = self.handle_events()
            
            # Update physics
            self.update_simulation()
            
            # Render frame
            self.render_frame()
            
            # Performance tracking
            frame_time = current_time - frame_start_time
            self.frame_times.append(frame_time)
            if len(self.frame_times) > 60:
                self.frame_times.pop(0)
            
            self.current_fps = 1.0 / max(frame_time, 0.001)
            frame_start_time = current_time
            
            # Control frame rate
            self.clock.tick(self.target_fps)
        
        pygame.quit()
        sys.exit()

def main():
    """Enhanced entry point"""
    try:
        print("🌟 Initializing Enhanced Three-Body Simulation...")
        renderer = AdvancedRenderer()
        renderer.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()