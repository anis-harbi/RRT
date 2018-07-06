import sys, random, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2


#constants
XDIM = 600
YDIM = 600
WINSIZE = [XDIM, YDIM]
EPSILON = 6.0
OBS=[[(0,25),(35,25),(35,64),(0,64)],
     [(110,0),(185,0),(185,54),(110,54)],
     [(360,0),(516,0),(516,44),(360,44)],
     [(0,165),(38,165),(38,320),(0,320)],
     [(111,90),(258,90),(258,73),(285,73),(285,90),(405,90),(405,119),(285,119),(285,155),(258,155),(258,119),
      (175,119),(175,193),(230,193),(230,293),(102,293),(102,192),(148,192),(148,119),(111,119)],
     [(490,73),(598,73),(598,120),(490,120)],
     [(535,156),(563,156),(563,193),(535,193)],
     [(435,165),(489,165),(489,239),(598,239),(598,275),(489,275),(489,310),(435,310)],
     [(268,304),(294,304),(294,340),(268,340)],
     [(323,174),(351,174),(351,378),(545,378),(545,404),(351,404),(351,560),(323,560),(323,404),(176,404),(176,378),(323,378)],
     [(66,388),(102,388),(102,452),(257,452),(257,487),(102,487),(102,543),(65,543),(65,561),(0,561),(0,516),(66,516)],
     [(223,534),(268,534),(268,598),(223,598)],
     [(388,452),(498,452),(498,553),(462,553),(462,497),(435,497),(435,597),(415,597),(415,497),(388,497)]]

def obsDraw(pygame,screen):
    blue=(0,0,255)
    for obs in OBS:
        pygame.draw.lines(screen,blue,True,obs)

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def scaled(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def chooseParent(nn,newnode):
    newnode.parent=nn
    return newnode,nn


def drawSolutionPath(start,goal,nodes,pygame,screen):
    pink = 200, 20, 240
    nn = nodes[0]
    for p in nodes:
        if dist([p.x,p.y],[goal.x,goal.y]) < dist([nn.x,nn.y],[goal.x,goal.y]):
            nn = p
    while nn!=start:
        pygame.draw.line(screen,pink,[nn.x,nn.y],[nn.parent.x,nn.parent.y],5)
        nn=nn.parent


class Node:
    x = 0
    y = 0
    parent=None
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

def checkIntersect(nodeA,nodeB,OBS):
    A=[nodeA.x,nodeA.y]
    B=[nodeB.x,nodeB.y]
    for obs in OBS:
      for i in range(len(obs)):
          if i < len(obs)-1:
              C=obs[i]
              D=obs[i+1]
          else:
              C=obs[i]
              D=obs[0]
          AC=[C[0]-A[0],C[1]-A[1]]
          AB=[B[0]-A[0],B[1]-A[1]]
          AD=[D[0]-A[0],D[1]-A[1]]
          BC=[C[0]-B[0],C[1]-B[1]]
          DC=[C[0]-D[0],C[1]-D[1]]
          if (AC[0]*AB[1]-AC[1]*AB[0])*(AD[0]*AB[1]-AD[1]*AB[0])<=0 and (DC[0]*AC[1]-DC[1]*AC[0])*(DC[0]*BC[1]-DC[1]*BC[0])<=0:
              return False
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('team25_lab5_2')
    white = 255, 255, 255
    black = 20, 20, 40
    green = 0,255,0
    pink = 200,20,240
    screen.fill(white)
    obsDraw(pygame,screen)
    nodes_start = []

    nodes_start.append(Node(56.0,18.0))
    start=nodes_start[0]

    nodes_goal = []
    nodes_goal.append(Node(448.0,542.0))
    goal=nodes_goal[0]

    pygame.draw.circle(screen,green,[int(start.x),int(start.y)],5)
    pygame.draw.circle(screen,green,[int(goal.x),int(goal.y)],5)

    a=1
    Goal=nodes_start[0]
    while a==1:
        rand = Node(random.random()*XDIM, random.random()*YDIM)
        nn = nodes_start[0]
        for p in nodes_start:
            if dist([p.x,p.y],[rand.x,rand.y]) < dist([nn.x,nn.y],[rand.x,rand.y]):
                nn = p
        interpolatedNode= scaled([nn.x,nn.y],[rand.x,rand.y])
        newnode = Node(interpolatedNode[0],interpolatedNode[1])
        if checkIntersect(nn,newnode,OBS):
            [newnode,nn]=chooseParent(nn,newnode)
            nodes_start.append(newnode)
            pygame.draw.line(screen,black,[nn.x,nn.y],[newnode.x,newnode.y])
            pygame.display.update()

            for node in nodes_goal:
                if (node.x-newnode.x)**2+(node.y-newnode.y)**2<=36:
                    Goal = node
                    pygame.draw.line(screen,pink,[newnode.x,newnode.y],[Goal.x,Goal.y],5)
                    a=0
                    break

                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit()
        if a==0:
            break

        rand = Node(random.random()*XDIM, random.random()*YDIM)
        mm = nodes_goal[0]
        for p in nodes_goal:
            if dist([p.x,p.y],[rand.x,rand.y]) < dist([mm.x,mm.y],[rand.x,rand.y]):
                mm = p
        interpolatedNode= scaled([mm.x,mm.y],[rand.x,rand.y])
        newnode = Node(interpolatedNode[0],interpolatedNode[1])
        if checkIntersect(mm,newnode,OBS):
            [newnode,mm]=chooseParent(mm,newnode)
            nodes_goal.append(newnode)
            pygame.draw.line(screen,black,[mm.x,mm.y],[newnode.x,newnode.y])
            pygame.display.update()

            for node in nodes_start:
                if (node.x-newnode.x)**2+(node.y-newnode.y)**2<=36:
                    Goal = node
                    pygame.draw.line(screen,pink,[newnode.x,newnode.y],[Goal.x,Goal.y],5)
                    a=0
                    break

                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit()

    drawSolutionPath(start,Goal,nodes_start,pygame,screen)
    drawSolutionPath(goal,Goal,nodes_goal,pygame,screen)
    pygame.display.update()

if __name__ == '__main__':
    main()
    running = True
    while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
                 running = False
