from vpython import*

''' Constant '''
g=vector(0,-10,0) # 題目給的重力加速度
size=0.8
dt=0.001
t=0

''' 建立物件 '''
scene=canvas(width=600,height=600,x=0,y=0,center=vector(0,15,0),background=vector(0.8,0.8,0.8))

floor=box(pos=vector(0,-size,0),length=20,height=0.01,width=10,color=color.blue) 

ball=sphere(pos=vector(0,0,0),radius=size,color=color.red,v=vector(0,20,0))

v_arrow=arrow(pos=ball.pos+vector(2,0,0),axis=ball.v*0.15,color=color.red) #球速的箭頭


while True:
    rate(1/dt)
    t+=dt
    
    ball.pos+=ball.v*dt
    ball.v+=g*dt
    v_arrow.pos=ball.pos+vector(2,0,0)
    v_arrow.axis=0.15*ball.v
    
    ''' 落地反彈 '''
    if ball.pos.y<=size and ball.v.y<=0:
        ball.v.y=-ball.v.y
        ball.v.y*=0.9 #反彈消耗能量 -> 速度變小
    
    '''停止條件'''
    if round( ball.v.y ) == 0 and ball.pos.y == 0:
        break 