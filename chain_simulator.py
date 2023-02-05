import pygame, math
from sys import exit


pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption('Chain Simulator')

def goTo(x,y):
    """Convert coordinates to be more like a standard xy graph
    
    Pygame's coordinate system is laid out where (0,0) is in the top left of the screen
    and values in the y axis increase as you go down.
    This function converts it to something more logical (at least for me) where
    (0,0) is at the centre of the screen with x values increasing to the
    right and y values increase as you go up.
    """
    x += (screen.get_width())//2
    y -= (screen.get_height())//2
    y = y*-1
    return (x,y)

# Does the inverse of goTo
def comeFrom(x,y):
    """Convert coordinates from the 'goTo' system back to the default
    
    See goTo function for more details
    """
    x -= (screen.get_width())//2
    y -= (screen.get_height())//2
    y = y*-1
    return (x,y)

def distance(x1,y1,x2,y2):
    """Get the distance between two points"""
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def goTowards(x1,y1,x2,y2):
    xv = ((x1-x2))/(distance(x1,y1,x2,y2))
    yv = ((x1-x2))/(distance(x1,y1,x2,y2))
    return xv,yv

class node:
    def __init__(self,x,y,xv,yv,mass: float = 1):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.mass = mass
    def draw(self):
        pygame.draw.circle(screen,(255,0,0),goTo(self.x,self.y),10)

chain = []
for i in range(8):
    chain.append(node(0,0,0,0))

k = 5 # Elasticity / speed of sound in the chain
chain[0].yv = 1
pygame.mouse.set_pos(goTo(0,0))
pygame.mouse.set_visible(True)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    mousepos = pygame.mouse.get_pos()
    mousepos = comeFrom(mousepos[0],mousepos[1])
    key_input = pygame.key.get_pressed()
    mouse_input = pygame.mouse.get_pressed()

    #game code
    screen.fill((255,255,255))
    pygame.draw.circle(screen,(127,127,127),goTo(0,0),300)
    pygame.draw.line(screen,(0,0,0),goTo(-400,0),goTo(400,0))
    if mouse_input[0] and distance(mousepos[0],mousepos[1],chain[0].x,chain[0].y) < 40:
        chain[0].xv,chain[0].yv = (mousepos[0]-chain[0].x,mousepos[1]-chain[0].y)
    if key_input[pygame.K_LEFT] or key_input[pygame.K_a]:
        chain[len(chain)-1].xv -= 5
    if key_input[pygame.K_RIGHT] or key_input[pygame.K_d]:
        chain[len(chain)-1].xv += 5
    if key_input[pygame.K_UP] or key_input[pygame.K_w]:
        chain[len(chain)-1].yv += 5
    if key_input[pygame.K_DOWN] or key_input[pygame.K_s]:
        chain[len(chain)-1].yv -= 5
    for link in chain:
        link.yv -= 1
        if distance(link.x,link.y,0,0) > 300: # Bring nodes back inwards if they get past this radius
            link.xv -= ((link.x-0)/distance(0,0,link.x,link.y))*(distance(0,0,link.x,link.y)-300)
            link.yv -= ((link.y-0)/distance(0,0,link.x,link.y))*(distance(0,0,link.x,link.y)-300)
        link.x += link.xv # Change the x and y position by the x and y velocity respectively
        link.y += link.yv
        link.xv *= 0.99 # Friction
        link.yv *= 0.99
        link.draw()
        if key_input[pygame.K_x]:
            link.xv = 0
            link.yv = 0
    for i in range(len(chain)-1,0,-1):# Force propogates down the chain. Makes each node attracted to the one before it
        if distance(chain[i].x+chain[i].xv,chain[i].y+chain[i].yv,chain[i-1].x,chain[i-1].y) > 20: # Bring the node closer if it gets too far
            chain[i].xv -= ((chain[i].x-chain[i-1].x)/k*chain[i].mass)-((chain[i].x-chain[i-1].x)/k*chain[i].mass)/(distance(chain[i].x,chain[i].y,chain[i-1].x,chain[i-1].y)*20)
            chain[i].yv -= ((chain[i].y-chain[i-1].y)/k*chain[i].mass)-((chain[i].y-chain[i-1].y)/k*chain[i].mass)/(distance(chain[i].x,chain[i].y,chain[i-1].x,chain[i-1].y)*20)
            chain[i].xv *= 0.99
            chain[i].yv *= 0.99
        elif distance(chain[i].x,chain[i].y,chain[i-1].x,chain[i-1].y) != 0:# Send the node further out if it gets too close
            chain[i].xv -= ((chain[i].x-chain[i-1].x))/(distance(chain[i].x,chain[i].y,chain[i-1].x,chain[i-1].y)*10)
            chain[i].yv -= ((chain[i].y-chain[i-1].y))/(distance(chain[i].x,chain[i].y,chain[i-1].x,chain[i-1].y)*10)
            chain[i].xv *= 0.99
            chain[i].yv *= 0.99
        pygame.draw.line(screen,(0,0,0),goTo(chain[i].x,chain[i].y),goTo(chain[i-1].x,chain[i-1].y))
    for i in range(0,len(chain)-1):#    Force propogates up the chain. Makes each node attracted to the one after it
        if distance(chain[i].x+chain[i].xv,chain[i].y+chain[i].yv,chain[i+1].x,chain[i+1].y) > 20:
            chain[i].xv -= ((chain[i].x-chain[i+1].x)/k*chain[i].mass)-((chain[i].x-chain[i+1].x)/k*chain[i].mass)/(distance(chain[i].x,chain[i].y,chain[i+1].x,chain[i+1].y)*20)
            chain[i].yv -= ((chain[i].y-chain[i+1].y)/k*chain[i].mass)-((chain[i].y-chain[i+1].y)/k*chain[i].mass)/(distance(chain[i].x,chain[i].y,chain[i+1].x,chain[i+1].y)*20)
            chain[i].xv *= 0.99
            chain[i].yv *= 0.99
        elif distance(chain[i].x,chain[i].y,chain[i+1].x,chain[i+1].y) != 0:
            chain[i].xv -= ((chain[i].x-chain[i+1].x))/(distance(chain[i].x,chain[i].y,chain[i+1].x,chain[i+1].y)*10)
            chain[i].yv -= ((chain[i].y-chain[i+1].y))/(distance(chain[i].x,chain[i].y,chain[i+1].x,chain[i+1].y)*10)
            chain[i].xv *= 0.99
            chain[i].yv *= 0.99

    pygame.display.update()
    clock.tick(60)