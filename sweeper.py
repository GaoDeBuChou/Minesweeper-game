import pygame,sys,random,operator
from pygame.locals import *

WHITE=(255,255,255)
BLACK=(0,0,0)
GREY=(220,220,220)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)

def bomber(length,width,bomb,m,n): #随机炸弹位置
    x=0
    y=0
    bombs=[]
    forbidden=((m-1,n-1),(m-1,n),(m-1,n+1),(m,n-1),(m,n),(m,n+1),(m+1,n-1),(m+1,n),(m+1,n+1))
    #扫雷中，第一次点击的位置必须为空地，且周围也无地雷
    for i in range(0,bomb):
        x = random.randint(0, length - 1)
        y = random.randint(0, width - 1)
        while (x,y) in bombs or (x,y) in forbidden:
            x = random.randint(0, length - 1)
            y = random.randint(0, width - 1)
        bombs.append((x,y))
    return bombs

def cal(length,width,bombs): #确定数字
    cals= [[0 for i in range(width)]for i in range(length)] #***深拷贝***
    for i in range(0,length):
        for j in range(0,width):
            if (i,j) not in bombs:
                for m in (i-1,i,i+1):
                    for n in (j-1,j,j+1):
                        if (m,n) in bombs:
                            cals[i][j]+=1
    return cals

def position(mousex,mousey,length,width): #鼠标点击事件
    x=(mousex-20)//15
    y=(mousey-40)//15
    if x>=0 and x<length:
        if y>=0 and y<width:
            return(x,y)
    return(-1,-1)

def open(x,y,cals,shown,length,width): #空地展开
    for m in (x-1,x,x+1):
        for n in (y-1,y,y+1):
            if (x,y)==(m,n):
                pass
            else:
                if m >= 0 and m < length and n >= 0 and n < width:
                    if (m,n) not in shown:
                        shown.append((m,n))
                        if cals[m][n] == 0:
                            open(m,n,cals,shown,length,width)
    return shown

def doubleclick(x,y,bombs,cal,flags): #快捷键
    temp=0
    for m in (x - 1, x, x + 1):
        for n in (y - 1, y, y + 1):
            if (m,n) in flags:
                temp+=1
    if temp==cal:
        for m in (x - 1, x, x + 1):
            for n in (y - 1, y, y + 1):
                if (m, n) in bombs:
                    if (m, n) not in flags:
                        return 0
        return 1
    else:
        return -1

def main():
    length = 9  # （横向）
    width = 9  # （纵向）

    pygame.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((length*15+40, width*15+60+20), 0, 32)
    pygame.display.set_caption('扫雷')

    oneImg = pygame.image.load('1.bmp')
    twoImg = pygame.image.load('2.bmp')
    threeImg = pygame.image.load('3.bmp')
    fourImg = pygame.image.load('4.bmp')
    fiveImg = pygame.image.load('5.bmp')
    sixImg = pygame.image.load('6.bmp')
    sevenImg = pygame.image.load('7.bmp')
    eightImg = pygame.image.load('8.bmp')
    flagImg = pygame.image.load('flag.bmp')
    notsureImg = pygame.image.load('notsure.bmp')

    font1 = pygame.font.SysFont("simsunnsimsun", 15)
    time1 = font1.render('时间：0', True, BLACK, GREY)
    rect1 = time1.get_rect()
    rect1.center = (50, 20)
    bomb1 = font1.render('炸弹：0', True, BLACK, GREY)
    rect2 = bomb1.get_rect()
    rect2.center = (length*15-10, 20)
    easy1 = font1.render('简单', True, GREEN, GREY)
    rect3 = easy1.get_rect()
    rect3.center = (30, width*15+50)
    normal1 = font1.render('中等', True, YELLOW, GREY)
    rect4 = normal1.get_rect()
    rect4.center = (80, width*15+50)
    hard1 = font1.render('困难', True, RED, GREY)
    rect5 = hard1.get_rect()
    rect5.center = (130, width*15+50)

    game = 2  # 0游戏失败 1游戏中 2游戏刚开始
    diffculty=1 #1简单2中等3困难

    bomb = 10
    bombs=[] #地雷位置
    shown=[] #玩家已翻开并确认的位置（空地，数字）
    time=0
    second=0
    cals= [[0 for i in range(width)]for i in range(length)] #***深拷贝***
    bombed=0 #游戏失败
    flag=[] #旗帜标记
    notsure=[] #问号标记

    x = 0
    y = 0 #临时变量
    red=(-1,-1) #爆炸点

    while True:
        DISPLAYSURF.fill(GREY)
        for i in range(0, length+1):
            pygame.draw.line(DISPLAYSURF, BLACK, (20+i*15,40), (20+i*15,40+width*15), 1)
        for i in range(0, width + 1):
            pygame.draw.line(DISPLAYSURF, BLACK, (20,40+i*15), (20+length*15,40+i*15), 1)

        for (i,j) in shown:
            if cals[i][j]==0:
                pygame.draw.rect(DISPLAYSURF,WHITE,(21+i*15,41+j*15,14,14),0)
            if cals[i][j]==1:
                DISPLAYSURF.blit(oneImg,(22+i*15,42+j*15))
            if cals[i][j]==2:
                DISPLAYSURF.blit(twoImg,(22+i*15,42+j*15))
            if cals[i][j]==3:
                DISPLAYSURF.blit(threeImg,(22+i*15,42+j*15))
            if cals[i][j]==4:
                DISPLAYSURF.blit(fourImg,(22+i*15,42+j*15))
            if cals[i][j]==5:
                DISPLAYSURF.blit(fiveImg,(22+i*15,42+j*15))
            if cals[i][j]==6:
                DISPLAYSURF.blit(sixImg,(22+i*15,42+j*15))
            if cals[i][j]==7:
                DISPLAYSURF.blit(sevenImg,(22+i*15,42+j*15))
            if cals[i][j]==8:
                DISPLAYSURF.blit(eightImg,(22+i*15,42+j*15))
        for (i, j) in flag:
            DISPLAYSURF.blit(flagImg, (22 + i * 15, 42 + j * 15))
        for (i, j) in notsure:
            DISPLAYSURF.blit(notsureImg, (22 + i * 15, 42 + j * 15))

        if bombed:
            for (i,j) in bombs:
                pygame.draw.circle(DISPLAYSURF,BLACK,(28+i*15,48+j*15),6)
            pygame.draw.circle(DISPLAYSURF, RED, (28 + red[0] * 15, 48 + red[1] * 15), 6)

        if game==0 and bombed==0: #胜利
            bomb=0
            for (i,j) in bombs:
                pygame.draw.rect(DISPLAYSURF, GREEN, (21+i*15,41+j*15,14,14))
                pygame.draw.circle(DISPLAYSURF,BLACK,(28+i*15,48+j*15),6)

        time1 = font1.render('时间：'+str(second), True, BLACK, GREY)
        DISPLAYSURF.blit(time1, rect1)
        bomb1 = font1.render('炸弹：' + str(bomb), True, BLACK, GREY)
        DISPLAYSURF.blit(bomb1, rect2)
        DISPLAYSURF.blit(easy1, rect3)
        DISPLAYSURF.blit(normal1, rect4)
        DISPLAYSURF.blit(hard1, rect5)

        if game!=0:
            time+=1
            if time%30==0:
                second+=1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                (x, y) = position(mousex, mousey, length, width)
                pressed=pygame.mouse.get_pressed() #0左键 1中键 2右键
                if x >= 0 and x < length and y >= 0 and y < width:
                    if pressed[0] and pressed[2]: #快捷键
                        if game == 1 and cals[x][y] > 0 and (x,y) in shown:
                            temp=doubleclick(x,y,bombs,cals[x][y],flag)
                            if temp==0: #判断失误，游戏结束
                                bombed = 1
                                game = 0
                                red = (-10,-10) #不显示
                                pygame.mixer.music.load('001.wav')
                                pygame.mixer.music.play()
                            if temp==1: #判断正确，周边展开
                                for m in (x - 1, x, x + 1):
                                    for n in (y - 1, y, y + 1):
                                        if m>=0 and m<length and n>=0 and n<width:
                                            if (m,n) not in bombs and (m,n) not in shown:
                                                shown.append((m,n))
                                                if cals[m][n]==0:
                                                    shown = open(m, n, cals, shown, length, width)
                                if length * width - len(shown) == len(bombs):  # 胜利条件：翻开所有非地雷的格子
                                    game = 0
                                    pygame.mixer.music.load('002.mid')
                                    pygame.mixer.music.play()

                    if pressed[0] and pressed[2]==0 and (x,y) not in flag and (x,y) not in notsure:
                        if game == 1:
                            if (x,y) not in shown:
                                if (x,y) in bombs: #踩雷死
                                    bombed=1
                                    game=0
                                    red=(x,y)
                                    pygame.mixer.music.load('001.wav')
                                    pygame.mixer.music.play()
                                else:
                                    shown.append((x, y))
                                    if cals[x][y] == 0:#周围无地雷，展开
                                        shown=open(x,y,cals,shown,length,width)

                            if length * width - len(shown) == len(bombs):  # 胜利条件：翻开所有非地雷的格子
                                game = 0
                                pygame.mixer.music.load('002.mid')
                                pygame.mixer.music.play()

                        elif game==2:
                            game=1
                            bombs = bomber(length, width, bomb, x, y)
                            cals = [[0 for i in range(width)] for i in range(length)]  # ***深拷贝***
                            cals = cal(length, width, bombs)  # 存数字

                            shown.append((x, y))
                            shown=open(x,y,cals,shown,length,width)#空地，展开
                        else:
                            game = 2
                            bombed = 0
                            if diffculty==1:
                                length = 9
                                width = 9
                                bomb = 10
                            elif diffculty==2:
                                length = 16
                                width = 16
                                bomb = 40
                            else:
                                length = 16
                                width = 30
                                bomb = 99
                            bombs = []  # 地雷位置
                            shown = []  # 玩家已翻开并确认的位置（空地，数字）
                            time = 0
                            second = 0
                            flag = []
                            notsure = []

                    if pressed[2] and pressed[0]==0:
                        if game == 1:
                            if (x,y) not in shown:
                                if (x,y) not in flag:
                                    if (x,y) not in notsure: #空地
                                        flag.append((x,y))
                                        bomb-=1
                                    else:
                                        notsure.remove((x,y))
                                else: #已有旗帜
                                    bomb+=1
                                    flag.remove((x,y))
                                    notsure.append((x,y))

                if mousex>15 and mousex<45 and mousey>width*15+42 and mousey<width*15+58: #点击'简单'
                    diffculty=1
                    game = 2
                    bombed = 0
                    length = 9  # （横向）
                    width = 9  # （纵向）
                    bomb = 10
                    bombs = []  # 地雷位置
                    shown = []  # 玩家已翻开并确认的位置（空地，数字）
                    time = 0
                    second = 0
                    flag = []
                    notsure = []
                    DISPLAYSURF = pygame.display.set_mode((length * 15 + 40, width * 15 + 60 + 20), 0, 32)
                    rect3.center = (30, width * 15 + 50)
                    rect4.center = (80, width * 15 + 50)
                    rect5.center = (130, width * 15 + 50)
                elif mousex>65 and mousex<95 and mousey>width*15+42 and mousey<width*15+58: #点击'中等'
                    diffculty=2
                    game = 2
                    bombed = 0
                    length = 16
                    width = 16
                    bomb = 40
                    bombs = []
                    shown = []
                    time = 0
                    second = 0
                    flag = []
                    notsure = []
                    DISPLAYSURF = pygame.display.set_mode((length * 15 + 40, width * 15 + 60 + 20), 0, 32)
                    rect3.center = (30, width * 15 + 50)
                    rect4.center = (80, width * 15 + 50)
                    rect5.center = (130, width * 15 + 50)
                elif mousex>115 and mousex<145 and mousey>width*15+42 and mousey<width*15+58: #点击'困难'
                    diffculty=3
                    game = 2
                    bombed = 0
                    length = 16
                    width = 30
                    bomb = 99
                    bombs = []
                    shown = []
                    time = 0
                    second = 0
                    flag = []
                    notsure = []
                    DISPLAYSURF = pygame.display.set_mode((length * 15 + 40, width * 15 + 60 + 20), 0, 32)
                    rect3.center = (30, width * 15 + 50)
                    rect4.center = (80, width * 15 + 50)
                    rect5.center = (130, width * 15 + 50)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__=='__main__':
    main()
