import pygame
from network import Network 

width = 250
height = 250
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("client")

##static
colors = [(255,0,0),(0,255,0),(0,0,255),(23,47,75)]
##dynamic
players = {}

def redraw_window(win, players):
    win.fill((255,255,255))
    for player in players:
        p = players[player]
        pygame.draw.circle(win, p["color"], (p["x"], p["y"]), 10)
    
def main(main):

    global players
    server = Network()
    current_id = server.connect(name)
    players = server.send("get")

    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(60)
        player = players[current_id]
        vel = 3
        
        keys = pygame.key.get_pressed()

        data = ""

        if keys[pygame.K_LEFT]:
            player["x"] -= vel

        if keys[pygame.K_RIGHT]:
            player["x"] += vel

        if keys[pygame.K_UP]:
            player["y"] -= vel

        if keys[pygame.K_DOWN]:
            player["y"] += vel

        data = "move " + str(player["x"]) + " " + str(player["y"])

        players = server.send(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        redraw_window(win, players)
        pygame.display.update()
   
while True:
    name = input("Please enter your name: ")
    if 0 < len(name) < 20:
        break
    else:
        print("Error, must be between 1 and 19 characters")


main(name)