from richoutput import *
import pygame
import random
import math
import time

pygame.init()
pygame.mixer.init()

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Pygame Screen")

# Basic Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (105, 180, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Info holder
all_n = []
all_x = []
all_u = []
# all_rods = [] (Depreceated)
all_g_rods = []
all_b_rods = []
# Neutron Class and Spawn function

class Neutron():
    def __init__(self, xpos: int, ypos: int, thermal: bool):
        self.thermal = thermal
        self.color = GRAY
        self.width = 0 if self.thermal else 2
        self.radius = 4.0
        # Store precise position as floats to avoid truncation errors during movement
        self.x = float(xpos)
        self.y = float(ypos)
        self.rect = pygame.Rect(xpos - self.radius, ypos - self.radius, self.radius * 2, self.radius * 2)
        # Set a constant speed and randomize direction
        self.speed = 2 if self.thermal else 5
        self.speed_x = 0
        self.speed_y = 0

    def draw(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.rect.center, radius=self.radius, width=self.width)

    def update(self):
        # Update the precise floating-point positions
        self.x += self.speed_x
        self.y += self.speed_y

        # Update the rect's integer position from the floats for drawing and collision
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        # Bounce off the walls
        # if self.rect.left <= 0 or self.rect.right >= screen_width:
        #     self.speed_x *= -1
        # if self.rect.top <= 0 or self.rect.bottom >= screen_height:
        #     self.speed_y *= -1

    def get_info(self):
        return f"Neutron: Position ({self.rect.centerx}, {self.rect.centery}), Thermal: {self.thermal}"

def neutron(xpos: int, ypos: int, thermal: bool) -> None:
    neutron_obj = Neutron(xpos, ypos, thermal)
    angle = random.uniform(0, 2 * math.pi) # Use 2*pi for a full circle in radians
    neutron_obj.speed_x = neutron_obj.speed * math.cos(angle)
    neutron_obj.speed_y = neutron_obj.speed * math.sin(angle)
    all_n.append(neutron_obj)

def fission_event(origin: (int, int)) -> None:
    # Spawn 2 to 3 new fast (non-thermal) neutrons that go in random directions
    x, y = origin[0], origin[1]
    num_new_neutrons = random.randint(2, 3)
    # info(f"Spawning {num_new_neutrons} new fast neutrons from fission.")
    for _ in range(num_new_neutrons):
        neutron(x, y, thermal=False)
    return None

# Uranium atom

class Uranium():
    def __init__(self, xpos: int, ypos: int, U235: bool):
        self.is_U235 = U235
        self.color = LIGHT_BLUE
        self.width = 5 if not self.is_U235 else 0
        self.radius = 10.0
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
    return None

# Create the objects before the loop





# Lets make a class for graphite rods



class Graphite_Rod():
    def __init__(self, xpos: int, ypos: int):
        # Graphite rods shouldn't really be mutuable such as a
        # neutron or uranium, so its best to not have initalized mutable vars

        # I change my mind on the positioning part of it
        self.color = GRAY
        self.width = 3
        self.height = 700 # This will be the lenggth in respects of the y length
        self.length = 10 # This will be the width in respects of the x length
        self.center = (xpos, ypos)
        self.rect = pygame.Rect(self.center[0], self.center[1], self.length, self.height)
        self.neutron_slowed = [].__len__() # Empty list, potentially good for debugging during runtime
        self.speed_y = 0 # Changes vertical position

        # During run time, there will be preset positions of the rods,

    def draw(self, surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect, width=self.width)

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.bottom > screen_height - 50:
            self.rect.bottom = screen_height - 50
            self.speed_y = 0

        if self.rect.top < -850:
            self.rect.top = -850
            self.speed_y = 0

    def get_info(self):
        return f"Graphite Rod: Position: ({self.rect.centerx}, {self.rect.centery}), Neutrons Absorbed: {len(self.neutron_absorbed)}"

def graphite_rod(xpos: int, ypos: int) -> None:
    rod = Graphite_Rod(xpos, ypos)
    rod.draw(surface=screen)
    all_g_rods.append(rod)
    return None

# Boron Rod

class Boron_Rod():
    def __init__(self, xpos: int, ypos: int):
        self.original_y = ypos
        self.color = GRAY
        self.width = 0
        self.height = 900
        self.length = 10
        self.center = (xpos, ypos)
        self.rect = pygame.Rect(self.center[0], self.center[1], self.length, self.height)
        self.neutrons_absorbed = [].__len__()
        self.speed_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect, width=self.width)

    def update(self):
        self.rect.y += self.speed_y

        # if self.rect.y < 50:
        #     self.rect.y = 50
        #     self.speed_y = 0
        
        if self.rect.bottom > screen_height - 50:
            self.rect.bottom = screen_height - 50
            self.speed_y = 0

        if self.rect.top < -850:
            self.rect.top = -850
            self.speed_y = 0



    def get_info(self):
        return f"Boron Rod: Position: ({self.rect.centerx}, {self.rect.centery}), Neutrons Absorbed: {len(self.neutrons_absorbed)}"


def boron_rod(xpos: int, ypos: int) -> None:
    rod = Boron_Rod(xpos, ypos)
    rod.draw(surface=screen)
    all_b_rods.append(rod)



for i in range(21):
    if i % 2 ==0:
        boron_rod(43 + (45*i), 50)
    else:
        graphite_rod(43 + (45*i), 50)


clock = pygame.time.Clock()
running = True
SCRAM_ALARM = pygame.mixer.Sound("scram_alarm.mp3")
playing = False
scram_active = False

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
        
        if event.type == pygame.KEYDOWN:         
            if event.key == pygame.K_UP:
                for r in all_b_rods[:]:
                    r.speed_y = -1
            
            if event.key == pygame.K_DOWN:
                for r in all_b_rods[:]:
                    r.speed_y = 1

            if event.key == pygame.K_z:
                for r in all_g_rods[:]:
                    r.speed_y = -1
            if event.key == pygame.K_x:
                for r in all_g_rods[:]:
                    r.speed_y = 1
            
            
            


            if event.key == pygame.K_SPACE:
                for k in all_u:
                    all_u.remove(k)
                for n in all_n:
                    all_n.remove(n)
                for i in range(19):
                    for j in range(24):
                        uranium((25 + (45*j)), (50 + (50*i)), True)
            if event.key == pygame.K_s: # SCRAM!! EMERGENCY ROD INSERTION

                emer("TRIPPED RPS CHANNEL A AND B Simutaneously")
                emer(f"Reactor Trip State reported: Manual Trip")

                
                if not playing:
                    SCRAM_ALARM.play(-1) # Play in a loop
                    playing = True
                    scram_active = True
                for r in all_b_rods[:]:
                    r.speed_y = 2
                    
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                for r in all_b_rods[:]:
                    r.speed_y = 0
        

    if scram_active and all(r.rect.bottom >= screen_height - 50 for r in all_b_rods):
        SCRAM_ALARM.stop()
        playing = False
        scram_active = False
                    

    for n in all_n:
        n.update()
    
    for r in all_b_rods:
        r.update()

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
                    # done(f"FISSION! Thermal neutron collided with U-235 at ({u.rect.centerx}, {u.rect.centery})")
                    click_sound = pygame.mixer.Sound("click.mp3")
                    click_sound.play()
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

    for n in all_n[:]:
        for r in all_g_rods[:]:
            if not n.thermal and n.rect.colliderect(r.rect):
                # The neutron is not thermal, so it should be thermalized by the graphite.
                # We can also get the collision point.
                collision_rect = n.rect.clip(r.rect)
                # info(f"Fast neutron collided with graphite rod at {collision_rect.center}")


                # r.neutron_slowed.append(n)
                all_n.remove(n)

                neutron(collision_rect.centerx, collision_rect.centery, thermal=True)

        for r in all_b_rods[:]:
            if n.rect.colliderect(r.rect):
                collision_rect = n.rect.clip(r.rect)
                # info(f"Fast neutron collided with boron rod at {collision_rect.center}")
                all_n.remove(n)


    screen.fill(WHITE)

    for n in all_n:
        n.draw(screen)

    for u in all_u:
        u.draw(screen)

    for r in all_g_rods:
        r.draw(screen)
    for r in all_b_rods:
        r.draw(screen)

    pygame.display.flip()


    clock.tick(60)

# Quit Pygame
pygame.quit()
