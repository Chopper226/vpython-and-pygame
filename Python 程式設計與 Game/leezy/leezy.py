'''
遊戲名稱 : Leezy
作者 : 306 05 陳樂宇 ， 306 29 蔡明妡
遊戲規則 : 若遇到比較高的鬆餅或是上頭有叉子的鬆餅，就按下空白建跳躍吧 !
          P.S. 左上角可以看到目前的進度 ><
圖是自己畫ㄉ !
'''

import pygame, random, sys, time       
from pygame.locals import *      
from const import *
from pygame import mixer

class Stage:
    ''' Stage '''
    def __init__(self): #初始
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.image.load("leezy_start.png")
        self.countdown = True # 是否倒數計時
        self.Time=0 # 紀錄倒數計時的秒數
        self.score_1st = True
        self.record = 0
        self.game_status = "startgame"
        
    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Leezy")
        
    def show(self, obj, pos: tuple =(0, 0)): # 顯示
        self.screen.blit(obj, pos)
        
    def count(self):  # 倒數計時
        if self.countdown == True:
            self.Time+=1
            if self.Time%50 == 0 and self.Time!=150: #切換倒數背景
                self.background = pygame.image.load(f"leezy_{int(3-self.Time/50)}.png")               
            if self.Time == 150 : # 遊戲開始
                self.countdown = False
                self.background = pygame.image.load("leezy_background.png")
                self.game_status = "play"
                pygame.mixer.music.load("leezy_music_play.mp3")
                pygame.mixer.music.play()
                              
    def bar(self): # 進度條
        self.img = pygame.transform.scale(pygame.image.load('leezy.png'), (40, 40))
        self.length = 106
        pygame.draw.rect(self.screen, (200, 200, 200), (5, 100, self.length+10, 20))
        pygame.draw.rect(self.screen, (251, 174, 63), (5, 100, (player.current_block_index+1) % self.length, 20))
        self.font = pygame.font.SysFont(None, 20)
        self.text = self.font.render('%s %%' % str(int(((player.current_block_index+1) % self.length)/self.length*100)), True, (255, 0, 0))
                    
    def load_bgm(self): # 倒數音樂
        pygame.mixer.init()
        pygame.mixer.music.load("leezy_music_countdown.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
    
    def start_game(self): #遊戲開始畫面
        for event in pygame.event.get(): 
            if event.type == QUIT:  
                terminate() 
            if event.type == KEYDOWN:      
                if event.key == K_SPACE: 
                    stage.load_bgm() 
                    stage.game_status = "countdown"
                    self.background = pygame.image.load(f"leezy_3.png")
                    return
                                                        
    def end_game(self) : # 遊戲結束
        pygame.mixer.music.stop()
        self.background = pygame.image.load("leezy_end.png")
        font = pygame.font.SysFont(None, 150) 
        self.score = int(((player.current_block_index+1) % self.length)/self.length*100)
        
        if self.score == 100: # 給星星
            self.background = pygame.image.load("leezy_star3.png")
        elif self.score > 75:
            self.background = pygame.image.load("leezy_star2.png")
        elif self.score > 50:
            self.background = pygame.image.load("leezy_star1.png")
            
        drawText(str(int(((player.current_block_index+1) % self.length)/self.length*100))+'%', font, self.screen, 950, 110)
        
        if self.score_1st == False: #紀錄顯示
            self.font = pygame.font.SysFont(None, 100) 
            drawText(str(self.record)+'%', font, self.screen, 1030, 355)
        self.record = max(int(((player.current_block_index+1) % self.length)/self.length*100), self.record)

class Player:
    ''' Player '''
    def __init__(self , block_group=[]):
        self.block_group = block_group
        self.player = pygame.image.load("leezy.png")
        self.playerRect = self.player.get_rect()
        self.playerRect.center = Player_pos   
        self.jumpjump = False # 下一個有沒有陷阱，有的話如果 jumpjump == 0 就可以按空白跳躍
        self.current_block_index = 0 # 現在的位置
        self.init_speed()
        self.min_height =self.set_min_height() # 要跳到的 y 位子
        self.is_up = False # 是否正在往上
        self.is_down = False # 是否正在往下
        self.not_jump = True  # 是否正在跳躍
        self.move = True # 磚塊是否可以移動
        
    def init_speed(self) : # 速度設定
        self.v = Player_v[self.current_block().level][self.next_block().level]
        self.a = Player_a[self.current_block().level][self.next_block().level]
        '''
        Player_v = [現在的 pancake 高度][下一個的 pancake 高度] # 初速
        Player_a  = [現在的 pancake 高度][下一個的 pancake 高度] # 加速度
        Player_dt 短單位時間內變化量
        '''
    
    def update(self) :  # 玩家 y 位子更新
        if self.is_up : # 上升
            self.not_jump = False
            self.v += self.a*Player_dt
            self.playerRect.y += self.v*Player_dt
            if self.v >=0 :
                self.is_up = False
                self.is_down = True
                
        elif self.is_down : # 下降
            self.v += self.a*Player_dt
            self.playerRect.y += self.v*Player_dt
            if self.playerRect.centery >= self.min_height :
                self.playerRect.centery = self.min_height 
                self.min_height =self.set_min_height()
                self.not_jump = True
                self.is_down = False
                self.jumpjump = False 
                
    def current_block(self): #現在的位子
        try:
            return self.block_group[self.current_block_index]
        except:
            return None
            
    def next_block(self): #下一個的位子
        try:
            return self.block_group[self.current_block_index + 1]
        except:
            return None
        
    def set_min_height(self): #設定下一個位子的 y 要跳到哪
        try:
            return Block_top[self.next_block().level]
        except:
            return None
                
class Block:
    ''' Pancake '''
    def __init__(self, position , level, trap ):      
        self.level = level # 台階高低 ( 0 , 1 , 2 )
        self.trap = trap # 有無陷阱

        if trap :   #分別載入不同的圖片
            if level == 0 :
                self.block = pygame.image.load("leezy_pancake-1.png")
            elif level == 1 :
                self.block = pygame.image.load("leezy_pancake-2.png")
            elif level == 2 :
                self.block = pygame.image.load("leezy_pancake-3.png")
        else :
            if level == 0 :
                self.block = pygame.image.load("leezy_pancake1.png")
            elif level == 1 :
                self.block = pygame.image.load("leezy_pancake2.png")
            elif level == 2 :
                self.block = pygame.image.load("leezy_pancake3.png")
        self.rect = self.block.get_rect()
        self.rect.center = position
        
    def init_block(): # 建立地圖
        Block_group = []
        for index in enumerate( Block_list ):
            if trap[index[0]] == 1 :
                if Block_list[index[0]] == 0 : 
                    Block_group.append( Block( (First_block_pos[0]+ 140*index[0],Block_bottom[0] ),Block_list[index[0]],1) )
                elif Block_list[index[0]] == 1 :
                    Block_group.append( Block( (First_block_pos[0]+ 140*index[0],Block_bottom[1] ),Block_list[index[0]],1) )
                elif Block_list[index[0]] == 2 :
                    Block_group.append( Block( (First_block_pos[0]+ 140*index[0],Block_bottom[2] ),Block_list[index[0]],1) )
            else :
                if Block_list[index[0]] == 0 : 
                    Block_group.append( Block( (First_block_pos[0]+ 140*index[0],Block_bottom[0] ),Block_list[index[0]],0) )
                elif Block_list[index[0]] == 1 :
                    Block_group.append( Block( (First_block_pos[0]+ 140*index[0],Block_bottom[1] ),Block_list[index[0]],0) )
                elif Block_list[index[0]] == 2 :
                    Block_group.append( Block( (First_block_pos[0]+ 140*index[0],Block_bottom[2] ),Block_list[index[0]],0) )
        return Block_group    

def terminate():   #終止
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y): # 畫出文字
    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
        
def player_jump(player): # 玩家跳躍
    
    if (not player.next_block()) and player.current_block_index == len(Block_list): # 終止條件
        stage.game_status = "end"
        return

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE :
                if player.not_jump : # 按下空白建現在沒跳那就讓他跳
                    player.is_up = True 
                    player.init_speed() # 重新設定跳躍速度
                elif player.is_up and player.next_block().trap == 1 and player.jumpjump == False and player.playerRect.y < player.min_height-5 : # 遇到叉子的時候的跳躍
                    player.is_up = True 
                    player.v = -40
                    player.a = 17
                    player.jumpjump == True
                               
def block_move(player): # pancake 移動
    if player.move :
        move_x = 3.5
        for block in enumerate( player.block_group ):
            player.block_group[block[0]].rect.centerx -= move_x
            if block[0] == len(Block_list)-1 :
                if player.block_group[block[0]].rect.centerx <= First_block_pos[0] :
                    player.move = False
            
        if player.current_block().rect.right <= player.playerRect.left and ( player.is_up or player.is_down ): # 改變現在的位子
                player.current_block_index += 1        
                
        if player.next_block() :
            if player.current_block().level > player.next_block().level : #如果下一個比較現在低就自己往下
                if player.current_block().rect.right <= player.playerRect.left :
                    player.is_up = True
                    player.init_speed()  
                
            if player.current_block().level == player.next_block().level and player.playerRect.left >= player.current_block().rect.centerx : # 如果同樣高度就自己跳躍
                if not player.is_up and not player.is_down :
                    player.is_up = True
                    player.init_speed() 

def touch_block(player) : #碰撞
    if player.next_block() : #撞到下一個 pancake
        if player.playerRect.colliderect( player.next_block().rect ) :
            if not player.playerRect.centery == Block_top[player.current_block().level] :
                if player.is_up :
                    if player.playerRect.left <= player.next_block().rect.centerx and player.playerRect.left >= player.next_block().rect.left:
                        return True
                '''elif player.is_down :
                    if player.playerRect.centerx >= player.next_block().rect.left+50 :
                        return True'''
            elif ( (not player.is_up) and (not player.is_down) ) :
                if player.playerRect.centerx-30 >= player.current_block().rect.right :
                    return True
    if player.current_block().trap == 1 and player.jumpjump == False and player.playerRect.centery == player.min_height: # 撞到陷阱
            return True
    return False

def init() :  #遊戲初始化
    global block_group,player 
    block_group = Block.init_block()
    player = Player( block_group )
    player.init_speed()  
    
stage = Stage()
stage.init()
init()


while True:
    if stage.game_status == "startgame" : # 遊戲開始
        stage.show( stage.background, ( 0, 0 ) ) 
        stage.start_game()  
        
    elif stage.game_status == "countdown" : # 倒數計時
        stage.count()
        stage.show( stage.background, ( 0, 0 ) )
        for event in pygame.event.get():
            if event.type == QUIT: 
                terminate()
    
    elif stage.game_status == "play" : # 遊戲進行
        
        # 移動
        block_move( player ) 
        player_jump( player )
        player.update()
        
        #顯示
        stage.show( stage.background, ( 0, 0 ) )
        stage.show( player.player, tuple( player.playerRect ) )
        for i in block_group :
            stage.show( i.block, tuple( i.rect.center) )
        
        #進度條
        stage.bar()
        stage.show(stage.text, (245, 100))
        stage.show(stage.img, ((player.current_block_index+1)%stage.length, 80))
           
        #音樂結束遊戲就結束
        if not pygame.mixer.music.get_busy() :
            player.move = False
            if player.playerRect.centery >= player.min_height : 
                stage.game_status = "end"
        
        # 碰撞到遊戲就結束    
        if touch_block(player) :
            stage.game_status = "end"
            
    elif stage.game_status == "end":
       
        #顯示
        stage.show( stage.background, ( 0, 0 ) ) 
        stage.end_game() 
        
        # 等待玩家判斷
        for event in pygame.event.get():
            if event.type == QUIT : 
                terminate()
                
            if event.type == KEYDOWN :      
                if event.key == K_q :  # Q 離開
                    terminate()
                    
                elif event.key == K_r : # R 重新開始
                    stage.load_bgm() 
                    stage.game_status = "countdown"
                    stage.score_1st = False
                    stage.countdown = True
                    stage.Time=0
                    init()
                    stage.background = pygame.image.load(f"leezy_3.png")
            
    pygame.display.flip()
    