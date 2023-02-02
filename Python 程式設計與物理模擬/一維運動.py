from vpython import*
size=0.5

x=arrow(pos=vector(0,0,0), axis=vector(1,0,0),shaftwidth=0.02,color=color.black)
ball=sphere(pos=vector(0,0,0), radius=size, color=color.magenta, v=vector(2,0,0),a=vector(-0.5,0,0))
pic_1=graph(title='x vs t',width=300,height=300,xtitle='t',ytitle='x',
foreground=color.black,background=color.white,xmax=5,xmin=0,ymax=5,ymin=0, align='left')
x_t=gcurve(color=color.blue)
pic_2=graph(title='v vs t',width=300,height=300,xtitle='t',ytitle='x',
foreground=color.black,background=color.white,xmax=5,xmin=0,ymax=5,ymin=0, align='left')
v_t=gcurve(color=color.red)
pic_3=graph(title='a vs t',width=300,height=300,xtitle='t',ytitle='x',
foreground=color.black,background=color.white,xmax=5,xmin=0,ymax=3,ymin=-2, align='left')
a_t=gcurve(color=color.green)
dt=0.001
t=0
while t<=5:
    rate(1000)
    ball.pos=ball.pos+ball.v*dt
    ball.v+=ball.a*dt
    t=t+dt
    x_t.plot(pos=(t,ball.pos.x))
    v_t.plot(pos=(t,ball.v.x))
    a_t.plot(pos=(t,ball.a.x))




