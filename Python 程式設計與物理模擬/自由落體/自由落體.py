from vpython import*

''' Constant '''
g=vector(0,-9.8,0) #重力加速度
height=122.5 #球的初始高度
size=5
dt=0.0001
t=0

''' 建立物件 '''
scene=canvas(width=600,height=600,x=0,y=0,center=vector(0,height/2,0),background=vector(0.8,0.8,0.8))

floor=box(pos=vector(0,-0.01/2,0),length=200,height=0.01,width=100,color=color.blue) 

ball=sphere(pos=vector(0,height+size,0),radius=size,color=color.red,v=vector(0,0,0))

while ball.pos.y-size>floor.pos.y: #讓球接觸到地板就停止
    rate(1/dt)
    t+=dt
    ball.pos+=ball.v*dt
    ball.v+=g*dt 
    
print('time =',round(t,2)) #輸出運行時間 ( 四捨五入制小數點後第二位 )