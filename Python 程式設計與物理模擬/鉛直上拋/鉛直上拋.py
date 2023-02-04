from vpython import*

''' Constant '''
g=vector(0,-10,0) # 題目給的重力加速度
size=0.5
dt=0.0005
t=0

''' 建立物件 '''
scene=canvas(width=600,height=600,x=0,y=0,center=vector(0,15,0),background=vector(0.8,0.8,0.8))

floor=box(pos=vector(0,0-size,0),length=20,height=0.01,width=10,color=color.blue) 

ball=sphere(pos=vector(0,0,0),radius=size,color=color.red,v=vector(0,20,0),make_trail=True,trail_type='points',interval=100)

# 畫出運動軌跡 : make_trail=True,trail_type='points',interval=100

''' 上升 '''
while ball.v.y>=0: #球的速度 = 0 -> 開始掉落
    rate(1/dt)
    t+=dt
    ball.pos+=ball.v*dt 
    ball.v+=g*dt
    
print('height =',round(ball.pos.y,2)) #輸出最大高度 ( 四捨五入至小數點後第二位 )
 
 
''' 下落 '''
while ball.pos.y-size>floor.pos.y: #球接觸到地板就停止
    rate(1/dt)
    t+=dt
    ball.pos+=ball.v*dt 
    ball.v+=g*dt 
    
print('time =',round(t,2)) #輸出運行時間 ( 四捨五入至小數點後第二位 )