import enum
import pygame
import random
class Colors(enum.Enum):
    shell    =0
    red     =1
    orange  =2
    yellow  =3
    green   =4
    blue    =5
    purple  =6
 
grid = [[0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],]
level_grid = [[0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],]
colors=[(10,70,100),             #shell
        (200,0,23),             #red
        (230,123,23),            #orange
        (220,220,10),            #yellow
        (23,232,23),            #green
        (23,150,250),            #blue
        (232,23,232),           #purple
        ]

TILE_COUNT=6
TILE_SIZE=66
TILE_MARGIN=7
GRID_SIZE=80
BORDER_SIZE=2
BOARD_OFFSET=10

STATE_SHOW_HINT=0
STATE_WAIT_USER=1
CURRENT_STATE=STATE_SHOW_HINT

SCREEN_W=TILE_COUNT*GRID_SIZE+2*BOARD_OFFSET
SCREEN_H=TILE_COUNT*GRID_SIZE+2*BOARD_OFFSET

COLOR_BG = (225,225,215)

score=0
level=1
wrong=False
level_finished=False
game_over=False
pickup_count=0

clock = None
s=None
sprite=None
pos=None
randomly_selected_tiles=[]
picked_tiles=[]

tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
pygame.font.init()
font = pygame.font.SysFont('Bebas', 72)
TEXT_GAMEOVER = font.render('GAME OVER', False, (0, 0, 0))


def init():

    pygame.init()
    
    global s
    s = pygame.display.set_mode((SCREEN_W,SCREEN_H))
    global pos
    pos=(0,0)
    global colors
    pygame.display.set_caption("COLOR TILES")
    s.fill(COLOR_BG)  
    global clock
    clock=pygame.time.Clock()
    clock.tick(30)

    generateLevel()


def getTilePos(mouse_pos):
    mouseX=mouse_pos[0]
    mouseY=mouse_pos[1]
    x=int((mouseX-BOARD_OFFSET)/GRID_SIZE)
    y=int((mouseY-BOARD_OFFSET)/GRID_SIZE)
    resX=-1
    resY=-1
    if x>=TILE_COUNT or y>= TILE_COUNT:
        return (resX,resY)
    if mouseX >= BOARD_OFFSET+TILE_MARGIN+x*GRID_SIZE and mouseX <= (x+1)*GRID_SIZE-TILE_MARGIN:
        resX=x
    if mouseY >= BOARD_OFFSET+TILE_MARGIN+y*GRID_SIZE and mouseY <= (y+1)*GRID_SIZE-TILE_MARGIN:
        resY=y
    return (resX,resY)


def selectLevelTiles():
    global level
    possible_pairs=[]
    for i in range(TILE_COUNT):
        for j in range(TILE_COUNT):
            possible_pairs.append((j,i))
    global randomly_selected_tiles
    randomly_selected_tiles=[]
    while len(randomly_selected_tiles)<level:
        random_pair=possible_pairs[random.randint(0,len(possible_pairs)-1)]
        randomly_selected_tiles.append(random_pair)
        possible_pairs.remove(random_pair)
def generateLevel():
    global level_grid
    for i in range(len(level_grid)):
        for j in range(len(level_grid[i])):
            level_grid[i][j]=random.randint(1,5)

def displayHint():
    global tile
    global level_grid
    global randomly_selected_tiles
    for pair in randomly_selected_tiles:
        x=pair[0]
        y=pair[1]
        tile.fill(colors[0])
        pygame.draw.rect(tile, colors[level_grid[y][x]], [BORDER_SIZE,BORDER_SIZE,TILE_SIZE-2*BORDER_SIZE,TILE_SIZE-2*BORDER_SIZE])
        s.blit(tile,(BOARD_OFFSET+x*GRID_SIZE+TILE_MARGIN,BOARD_OFFSET+y*GRID_SIZE+TILE_MARGIN))
    pygame.display.flip()



def hideHint():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            tile.fill(colors[0])
            pygame.draw.rect(tile, colors[grid[i][j]], [BORDER_SIZE,BORDER_SIZE,TILE_SIZE-2*BORDER_SIZE,TILE_SIZE-2*BORDER_SIZE])
            s.blit(tile,(BOARD_OFFSET+j*GRID_SIZE+TILE_MARGIN,BOARD_OFFSET+i*GRID_SIZE+TILE_MARGIN))
    pygame.display.flip()

def pickTile(pos):
    global s
    global tile
    global picked_tiles
    global level_grid
    global score
    if  pos != (-1,-1):
        if not pos in picked_tiles and len(picked_tiles)<level:
            picked_tiles.append(pos)
            pygame.draw.rect(tile, colors[level_grid[pos[1]][pos[0]]], [BORDER_SIZE,BORDER_SIZE,TILE_SIZE-2*BORDER_SIZE,TILE_SIZE-2*BORDER_SIZE])
            s.blit(tile,(BOARD_OFFSET+pos[0]*GRID_SIZE+TILE_MARGIN,BOARD_OFFSET+pos[1]*GRID_SIZE+TILE_MARGIN))
            pygame.display.flip()
            if not pos in randomly_selected_tiles:
                global game_over
                game_over=True
            else:
                global pickup_count
                pickup_count=pickup_count+1
                pygame.event.clear()
                score=score+1

def displayGameOverAlert():
    global s
    X = SCREEN_W
    Y = SCREEN_H
    frame= pygame.Surface((X, Y))
    pygame.draw.rect(frame, colors[0], (0,0,X,Y))
    text=font.render("GAME OVER",True,COLOR_BG)
    text_frame=text.get_rect()
    text_frame.center=(X/2,Y/2)
    s.blit(frame,frame.get_rect())
    s.blit(text,text_frame)
    pygame.display.flip()






def main():

    init()
    hideHint()
    while True:
        
        global level
        global level_finished
        global game_over
        global score
        global pickup_count
        game_started=False
        game_over=False
        level=1
        score=0
        while not game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type ==pygame.MOUSEBUTTONDOWN:
                    game_started=True
        
                            
        

        while not game_over:
            level_finished = False
            picked_tiles.clear()
            randomly_selected_tiles.clear()
            generateLevel()
            selectLevelTiles()    
            while not level_finished:
                pickup_count=0
                hideHint()  #kind of a reset
                displayHint()
                pygame.time.wait(3000*level)
                hideHint()
                start_ticks=pygame.time.get_ticks()
                pygame.event.clear()
                while ((pygame.time.get_ticks()-start_ticks)/1000<3*level) and (not game_over) and (pickup_count<level):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        if event.type ==pygame.MOUSEBUTTONDOWN:
                            pickTile(getTilePos(pygame.mouse.get_pos()))
                            
                level_finished=True
                game_over=len(picked_tiles)!=len(randomly_selected_tiles)
            level=level+1
        game_started=False
        displayGameOverAlert()
        print("Game over. Score: "+str(score))
    
main()