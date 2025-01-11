import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System with Three-Body Problem")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
GREEN = (34, 139, 34)
ORANGE = (255, 165, 0)
PURPLE = (138, 43, 226)

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6 * 1000 
    G = 6.67430e-11  
    SCALE = 250 / AU  
    TIMESTEP = 3600 * 1  

    def __init__(self, x, y, radius, color, mass, name=""):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * self.SCALE + WIDTH / 2
                py = py * self.SCALE + HEIGHT / 2
                updated_points.append((px, py))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

        if self.name:
            name_text = FONT.render(self.name, 1, WHITE)
            win.blit(name_text, (x - name_text.get_width() / 2, y - self.radius - 15))

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)} km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y + self.radius + 5))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        softening = 1e9
        distance = max(distance, softening)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "Sun")
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9722 * 10**24, "Earth")
    earth.y_vel = 29.78 * 1000

    satellite_distance = 0.01 * Planet.AU  
    satellite_mass = 1 * 10**22  
    satellite_orbital_velocity = math.sqrt(Planet.G * earth.mass / satellite_distance)

    satellite1 = Planet(earth.x - satellite_distance, earth.y, 6, GREEN, satellite_mass, "Satellite 1")
    satellite1.y_vel = earth.y_vel + satellite_orbital_velocity

    satellite2 = Planet(earth.x + satellite_distance, earth.y, 6, ORANGE, satellite_mass, "Satellite 2")
    satellite2.y_vel = earth.y_vel - satellite_orbital_velocity

    satellite3 = Planet(earth.x, earth.y + satellite_distance, 6, PURPLE, satellite_mass, "Satellite 3")
    satellite3.x_vel = earth.x_vel + satellite_orbital_velocity

    planets = [sun, earth, satellite1, satellite2, satellite3]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
