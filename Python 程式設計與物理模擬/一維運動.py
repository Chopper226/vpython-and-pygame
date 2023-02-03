from vpython import*

''' Constant '''
size=0.5
dt=0.001
t=0

''' 建立物件 '''
ball=sphere(pos=vector(0,0,0),radius=size,color=color.magenta,v=vector(4,0,0),a=vector(-2,0,0))

''' xt 圖 '''
pic_xt=graph(title='x vs t',width=300,height=300,xtitle='t',ytitle='x',foreground=color.black,background=color.white,xmax=5,xmin=0,ymax=5,ymin=-5,align='left')

x_t=gcurve(color=color.blue)

''' vt 圖 '''
pic_vt=graph(title='v vs t',width=300,height=300,xtitle='t',ytitle='v',foreground=color.black,background=color.white,xmax=5,xmin=0,ymax=6,ymin=-6,align='left')

v_t=gcurve(color=color.red)

''' at 圖 '''
pic_at=graph(title='a vs t',width=300,height=300,xtitle='t',ytitle='a',foreground=color.black,background=color.white,xmax=5,xmin=0,ymax=4,ymin=-4,align='left')

a_t=gcurve(color=color.green)


while t<=5:
    rate(1000)
        
    ''' 更改球的位置與速度'''
    ball.pos=ball.pos+ball.v*dt
    ball.v+=ball.a*dt
    
    t=t+dt # 經過時間
    
    ''' 畫圖'''
    x_t.plot(pos=(t,ball.pos.x))
    v_t.plot(pos=(t,ball.v.x))
    a_t.plot(pos=(t,ball.a.x))



