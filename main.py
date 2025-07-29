from richoutput import *
import pygame
import random
import math

pygame.init()


screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Pygame Screen")

# Basic Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (105, 180, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)

# Info holder
all_n = []
all_x = []
all_u = []
all_rods = []
# Neutron Class and Spawn function

class Neutron():
    def __init__(self, xpos: int, ypos: int, thermal: bool):
        self.thermal = thermal
        self.color = GRAY
        self.width = 0 if self.thermal else 2
        self.radius = 5.0
        self.rect = pygame.Rect(xpos - self.radius, ypos - self.radius, self.radius * 2, self.radius * 2)
        # Set a constant speed and randomize direction
        self.speed = 2 if self.thermal else 5
        self.speed_x = 0
        self.speed_y = 0
    
    def draw(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.rect.center, radius=self.radius, width=self.width)

    def update(self):
        # move_ip stands for "move in place"
        self.rect.move_ip(self.speed_x, self.speed_y)

        # Bounce off the walls
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            rand = random.uniform(-1.25, -0.75)
            self.speed_x *= rand
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            rand = random.uniform(-1.25, -0.75)
            self.speed_y *= rand

    def get_info(self):
        return f"Neutron: Position ({self.rect.centerx}, {self.rect.centery}), Thermal: {self.thermal}"

def neutron(xpos: int, ypos: int, thermal: bool) -> None:
    neutron_obj = Neutron(xpos, ypos, thermal)
    angle = random.uniform(0, 2 * math.pi)
    neutron_obj.speed_x = neutron_obj.speed * math.cos(angle)
    neutron_obj.speed_y = neutron_obj.speed * math.sin(angle)
    all_n.append(neutron_obj)
    if not thermal:
        warn("Neutron can't merge with u235, use graphite moderator to slow down neutron")
    else:
        info("Neutron can merge with u235")
    return None

def fission_event(origin: (int, int)) -> None:
    # Spawn 2 to 3 new fast (non-thermal) neutrons that go in random directions
    x, y = origin[0], origin[1]
    num_new_neutrons = random.randint(2, 3)
    info(f"Spawning {num_new_neutrons} new fast neutrons from fission.")
    for _ in range(num_new_neutrons):
        neutron(x, y, thermal=False) # Fission produces fast neutrons
    return None

# Uranium atom

class Uranium():
    def __init__(self, xpos: int, ypos: int, U235: bool):
        self.is_U235 = U235
        self.color = LIGHT_BLUE
        self.width = 5 if not self.is_U235 else 0
        self.radius = 20.0
        self.rect = pygame.Rect(xpos - self.radius, ypos - self.radius, self.radius * 2, self.radius * 2)
        self.speed = 1
        self.speed_x = 0
        self.speed_y = 0
    
    def draw(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.rect.center, radius=self.radius, width=self.width)

    def get_info(self):
        return f"Uranium: Position ({self.rect.centerx}, {self.rect.centery})"

def uranium(xpos: int, ypos: int, U235: bool) -> None:
    uranium_atom = Uranium(xpos, ypos, U235=U235)
    all_u.append(uranium_atom)
    uranium_atom.draw(surface=screen)
    info("Uranium atom spawned")
    return None

# Create the objects before the loop

uranium(screen_width // 2, screen_height // 2, True)
uranium(screen_width // 4, screen_height // 4, False)
uranium(screen_width * 3 // 4, screen_height * 3 // 4, True)



# Lets make a class for graphite rods 



class Graphite_Rod():
    def __init__(self):
        # Graphite rods shouldn't really be mutuable such as a
        # neutron or uranium, so its best to not have initalized mutable vars
        self.color = GRAY
        self.width = 3
        self.height = 500 # This will be the lenggth in respects of the y length
        self.length = 10 # This will be the width in respects of the x length
        center = (100, 100)
        self.rect = pygame.Rect(center[0], center[1], self.length, self.height)
        self.neutron_absorbed = [] # Empty list, potentially good for debugging during runtime
        self.speed_y = 0 # Changes vertical position

        # During run time, there will be preset positions of the rods,
        
    def draw(self, surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect, width=self.width)

    def get_info(self):
        return f"Graphite Rod: Position: ({self.rect.centerx}, {self.rect.centery}), Neutrons Absorbed: {len(self.neutron_absorbed)}"

def spawn_rod() -> None:
    rod = Graphite_Rod()
    rod.draw(surface=screen)
    all_rods.append(rod)
    info("Graphite rod spawned")
    return None



spawn_rod()
spawn_rod()
spawn_rod()

"""
For now, we do not need xenon, we are only observing this reaction at an atomic scale
we should get started on the logistics, how do it bounces off, etc
assuming neutrons (both thermal and fast) had a constant speed no matter what, we can just worry
about getting a proper random direction in the even of a fission
however, we need to first find a way to move these particals

This was completed ln 90-101 nd has moved next to the neutron class
"""

clock = pygame.time.Clock()
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if event.button == 1: # Left click
                neutron(x, y, True)
            elif event.button == 3: # Right click
                neutron(x, y, False)


    for n in all_n:
        n.update()

    # --- Collision Detection ---
    # We will check for collisions between neutrons and uranium atoms.
    # We iterate through copies of the lists because we might remove items from them.
    for n in all_n[:]:
        for u in all_u[:]:
            # For circles, a simple rect collision isn't very accurate.
            # A better way is to check the distance between their centers.
            dx = n.rect.centerx - u.rect.centerx
            dy = n.rect.centery - u.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance < n.radius + u.radius:
                # This is a collision!
                if n.thermal and u.is_U235:
                    # FISSION!
                    done(f"FISSION! Thermal neutron collided with U-235 at ({u.rect.centerx}, {u.rect.centery})")
                    
                    # The neutron is absorbed and the uranium atom is destroyed.
                    all_n.remove(n)
                    all_u.remove(u)

                    # Spawn new fast neutrons from the fission event.
                    fission_event(origin=(u.rect.centerx, u.rect.centery))

                    # Since this neutron is gone, break out of the inner loop
                    # and move to the next neutron.
                    break
                else:
                    # For other types of collisions, just bounce the neutron off.
                    n.speed_x *= -1
                    n.speed_y *= -1

    screen.fill(WHITE)  

    for n in all_n:
        n.draw(screen)
        
    for u in all_u:
        u.draw(screen)
    

    for r in all_rods:
        r.draw(screen)
    
    pygame.display.flip()


    clock.tick(60)

# Quit Pygame
pygame.quit()
