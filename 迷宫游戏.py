from tkinter import*
from tkinter import ttk,filedialog
import random
import time

class pos:#定义一个类用于记录位置
    def __init__(self,x,y,pre):#pre用于在广搜时记录前驱节点
        self.x=x
        self.y=y
        self.pre=pre
    def __eq__(self,other):#重载eq函数，坐标相同即为同一个对象
        return (self.x==other.x) and (self.y==other.y)
    def change(self,x,y,pre):#修改值
        self.x=x
        self.y=y
        self.pre=pre

class queue:#定义一个类用于队列操作
    def __init__(self):
        self.list=[]
        self.pos=-1                #队头
    def put(self,item):#入队
        self.list.append(item)
    def get(self):#出队
        self.pos=self.pos+1     #出队操作只是获取队头元素，并将队头向后移，保留前驱节点记录路径
        return self.list[self.pos]
    def size(self):#队列大小是队尾减去队头
        return len(self.list)-self.pos-1

width=0                       #一个迷宫格子的宽度
lenth=0                       #一个迷宫格子的长度
playflag=0                    #玩家完成游戏的标记
playerpathlength=0            #玩家完成游戏的路径长度
pcpathlength=0                #电脑玩家完成游戏的路径长度
inlet=pos(0,0,None)           #入口
outlet=pos(0,0,None)          #出口


def DFS(mapifo,curlet):#广度优先搜索寻找最短路径，地图信息mapifo，当前位置curlet
    _mapifo=[]                           #mapifo不允许修改
    for i in range(len(mapifo)):
        _mapifo.append(list(mapifo[i]))
    q=queue()
    entrance=curlet
    q.put(entrance)                      #初始化队列，第一个元素为当前位置
    _mapifo[curlet.x][curlet.y]='0'      #将所有曾经在队列中的元素对应的位置标记为'0'，避免再次入队
    m=len(_mapifo)
    n=len(_mapifo[0])-1
    while q.size() != 0:                 #队列不为空时
        a=q.get()                        #取出队头元素，依次访问周围四个位置，判断是否入队
        if (a.x-1) >= 0 and _mapifo[a.x-1][a.y]!='0':
            _mapifo[a.x-1][a.y]='0'
            b1=pos(a.x-1,a.y,a)
            q.put(b1)
            if b1==outlet: break         #发现入队元素中有出口位置，结束循环
        if (a.x+1) < m and _mapifo[a.x+1][a.y]!='0':
            _mapifo[a.x+1][a.y]='0'
            b2=pos(a.x+1,a.y,a)
            q.put(b2)
            if b2==outlet: break
        if (a.y-1) >= 0 and _mapifo[a.x][a.y-1]!='0':
            _mapifo[a.x][a.y-1]='0'
            b3=pos(a.x,a.y-1,a)
            q.put(b3)
            if b3==outlet: break
        if (a.y+1) < n and _mapifo[a.x][a.y+1]!='0':
            _mapifo[a.x][a.y+1]='0'
            b4=pos(a.x,a.y+1,a)
            q.put(b4)
            if b4==outlet: break
    path=[]
    if q.size()!=0:#队列为空说明不存在路径
        cur=q.list[-1]
        while cur != curlet:
            path.append(cur)
            cur=cur.pre #从出口开始逐次访问前驱节点，并加入path
    return path #path中第一个元素为出口，最后一个元素为当前位置的下一个位置

def pathlowcost(mapifo,mapcanva):#在画布上显示最短路径
    if playflag==0:
        texts='请先完成游戏'
    else:
        path=DFS(mapifo,inlet)           #获取最短路径，取当前位置为入口
        for i in range(len(path)):
            j=len(path)-i-1              #画圆
            mapcanva.create_oval((path[j].y+1/4)*lenth,(path[j].x+1/4)*width,(path[j].y+3/4)*lenth,(path[j].x+3/4)*width,fill='green')
        texts='最短路径需消耗步数:%d步'%len(path)
    lowcost=Toplevel(root)
    lowcost.geometry('320x120')
    lb = Label(lowcost,text=texts,font=('黑体',12,'bold'))
    lb.pack()

def pcpath(dif,mapifo):     #电脑玩家路径规划函数
    if playflag==0:
        pclb=Toplevel(root)
        pclb.geometry('320x120')
        lb = Label(pclb,text='请先完成游戏',font=('黑体',12,'bold'))
        lb.pack()
        return
    global pcpathlength
    pcpathlength=0
    difn=0                  #难度系数
    if dif=='简单':
        difn=0.5
    elif dif=='适中':
        difn=0.65
    elif dif=='困难':
        difn=0.8
    elif dif=='高难':
        difn=0.95
    else:
        difn=random.uniform(0.35,0.95)
    m=len(mapifo)
    n=len(mapifo[0])-1
    #print(m)
    #print(n)
    pcpos=pos(inlet.x,inlet.y,None)     #电脑玩家当前位置
    nextpos1=pos(pcpos.x,pcpos.y,None)  #电脑玩家下一次行动的可能位置，最多四个
    nextpos2=pos(pcpos.x,pcpos.y,None)
    nextpos3=pos(pcpos.x,pcpos.y,None)
    nextpos4=pos(pcpos.x,pcpos.y,None)
    while pcpos!=outlet:#当电脑玩家未到达终点时
        #print('%d %d'%(pcpos.x,pcpos.y))
        nexts=[]                             #电脑玩家下一次行动的可能位置的存储列表
        if (pcpos.x-1) >= 0 and mapifo[pcpos.x-1][pcpos.y]!='0':
            nextpos1.change(pcpos.x-1,pcpos.y,pcpos.pre)
            nexts.append(nextpos1)
        if (pcpos.x+1) < m and mapifo[pcpos.x+1][pcpos.y]!='0':
            nextpos2.change(pcpos.x+1,pcpos.y,pcpos.pre)
            nexts.append(nextpos2)
        if (pcpos.y-1) >= 0 and mapifo[pcpos.x][pcpos.y-1]!='0':
            nextpos3.change(pcpos.x,pcpos.y-1,pcpos.pre)
            nexts.append(nextpos3)
        if (pcpos.y+1) < n and mapifo[pcpos.x][pcpos.y+1]!='0':
            nextpos4.change(pcpos.x,pcpos.y+1,pcpos.pre)
            nexts.append(nextpos4)
        #print(len(nexts))
        if len(nexts) == 1:        #如果只有一个可能的位置，就选这个位置
            pcpos=nexts[0]
        else:
            path=DFS(mapifo,pcpos) #否则以当前位置发起搜索获取最短路径
            p=(random.random()+random.random()+random.random()+random.random()+random.random())/5
            #print(n)
            if p < difn:           #用难度系数决定电脑玩家下一位置是否走最短路径给出的下一位置
                pcpos=path[-1]
            else:#如果不走最短路径给出的下一位置，在列表中除去该位置外随机选择一个可能位置作为下一位置
                i=random.randint(0,len(nexts)-2) 
                if nexts[i] == path[-1]:i=i+1
                pcpos=nexts[i]
        #print(len(next))
        pcpathlength=pcpathlength+1 #电脑玩家步数+1
    pclb=Toplevel(root)
    pclb.geometry('320x120')
    if pcpathlength == playerpathlength:#判断是否取胜
        texts='你与电脑玩家旗鼓相当'
    elif pcpathlength > playerpathlength:
        texts='恭喜你，你战胜了电脑玩家'
    else:
        texts='很遗憾，你败给了电脑玩家'
    lb = Label(pclb,text='电脑玩家耗费步数:%d步\n%s'%(pcpathlength,texts),font=('黑体',12,'bold'))
    lb.pack()
    
def winshow():#玩家完成游戏后显示
    win=Toplevel(root)
    win.geometry('320x120')
    lb = Label(win,text='恭喜你完成迷宫游戏，耗费步数:%d步'%playerpathlength,font=('黑体',12,'bold'))
    lb.pack()

def leftmove(mapifo,curpos,mapcanva,player):#玩家左移函数
    global playerpathlength
    global playflag
    if playflag==1:return                  #游戏结束后不移动
    if curpos.y-1 < 0:return               #不能越界
    if mapifo[curpos.x][curpos.y-1] == '0':return  #不能前往不能到达的位置
    curpos.change(curpos.x,curpos.y-1,curpos.pre) #修改玩家位置
    playerpathlength=playerpathlength+1   #玩家步数+1
    mapcanva.coords(player,(curpos.y+1/4)*lenth,(curpos.x+1/4)*width,(curpos.y+3/4)*lenth,(curpos.x+3/4)*width)#画布上修改玩家位置
    if curpos==outlet: #判断玩家是否到达终点
        playflag=1
        winshow()
def rightmove(mapifo,curpos,mapcanva,player):#玩家右移函数
    global playerpathlength
    global playflag
    if playflag==1:return
    if curpos.y+1 >= len(mapifo[0])-1:return
    if mapifo[curpos.x][curpos.y+1] == '0':return
    curpos.change(curpos.x,curpos.y+1,curpos.pre)
    playerpathlength=playerpathlength+1
    mapcanva.coords(player,(curpos.y+1/4)*lenth,(curpos.x+1/4)*width,(curpos.y+3/4)*lenth,(curpos.x+3/4)*width)
    if curpos==outlet:
        playflag=1
        winshow()
def upmove(mapifo,curpos,mapcanva,player):#玩家上移函数
    global playerpathlength
    global playflag
    if playflag==1:return
    if curpos.x-1 < 0:return
    if mapifo[curpos.x-1][curpos.y] == '0':return
    curpos.change(curpos.x-1,curpos.y,curpos.pre)
    playerpathlength=playerpathlength+1
    mapcanva.coords(player,(curpos.y+1/4)*lenth,(curpos.x+1/4)*width,(curpos.y+3/4)*lenth,(curpos.x+3/4)*width)
    if curpos==outlet:
        playflag=1
        winshow()
def downmove(mapifo,curpos,mapcanva,player):#玩家下移函数
    global playerpathlength
    global playflag
    if playflag==1:return
    if curpos.x+1 >= len(mapifo):return
    if mapifo[curpos.x+1][curpos.y] == '0':return
    curpos.change(curpos.x+1,curpos.y,curpos.pre)
    playerpathlength=playerpathlength+1
    mapcanva.coords(player,(curpos.y+1/4)*lenth,(curpos.x+1/4)*width,(curpos.y+3/4)*lenth,(curpos.x+3/4)*width)
    if curpos==outlet:
        playflag=1
        winshow()

def pathcheck(mapifo):#检查迷宫是否存在通路的函数
    path=DFS(mapifo,inlet)
    if len(path)==0:
        texts='该迷宫不存在通路'
    else:
        texts='该迷宫存在通路'
    check=Toplevel(root)
    check.geometry('320x120')
    lb = Label(check,text=texts,font=('黑体',16,'bold'))
    lb.pack()

def randommap():#随机地图生成函数
    createflag=0 #随机地图生成成功的标记
    while createflag==0:
        m=random.randint(20,30)  #随机地图的大小
        n=random.randint(21,31)
        #print(m)
        #print(n)
        mapifo=[]
        for i in range(0,m):#随机地图填充
            mapifopart=[]
            for j in range(0,n):
                c='0'
                if random.randint(0,9) < 7:
                    c='1'
                mapifopart.append(c)
            mapifo.append(mapifopart)
        i=random.randint(0,int(m/4)) 
        j=random.randint(0,int(n/4))
        mapifo[i][j]='i'               #入口设置
        inlet.change(i,j,inlet.pre)
        i=(i+int(3*m/4))%m
        j=(j+int(3*n/4))%n
        if j == n:
            j=j-2
        mapifo[i][j]='o'               #出口设置
        outlet.change(i,j,outlet.pre)
        path=DFS(mapifo,inlet)
        if len(path)!=0: #判断生成的随机地图是否存在通路
            createflag=1
    return mapifo

def saving(mapifo,name,save):#将迷宫写入文件保存
    save.destroy()
    f=open('./maps/'+name+'.txt','a')
    for i in range(len(mapifo)):
        for j in range(len(mapifo[i])):
            f.write(mapifo[i][j])
        f.write('\n')
    f.close()

def mapsave(mapifo):#迷宫保存文件名获取
    save=Toplevel(root)
    save.geometry('240x120')
    lb = Label(save,text='迷宫名',font=('黑体',12,'bold'))
    lb.pack()
    inp=Entry(save)
    inp.pack()
    bt=Button(save,text='确定',command=lambda: saving(mapifo,inp.get(),save))
    bt.pack()

def mapcreate(dif,mapfile,mapset):  #游戏界面函数
    mapset.destroy()             #关闭地图和困难选择界面
    game=Toplevel(root)
    game.title('游戏')
    game.geometry('640x480')
    mapcanva=Canvas(game,width=480,height=480,background='white')#创建画布
    mapcanva.pack(side=LEFT)
    if mapfile == '':#判断是否需要随机生成地图
        mapifo=randommap()
    else:
        f = open(mapfile,'r')
        mapifo=f.readlines()
        f.close()
    global width
    global lenth
    global playflag
    global playerpathlength
    global pcpathlength
    playflag=0
    playerpathlength=0
    pcpathlength=0
    m=len(mapifo)
    n=len(mapifo[0])-1 #文件读取地图最后一位是回车符，不需要
    width=int(480/m) #确定宽度
    lenth=int(480/n) #确定长度
    for i in range(0,m):    #在画布上构建迷宫
        for j in range(0,n):
            if mapifo[i][j]=='1':
                mapcanva.create_rectangle(j*lenth,i*width,(j+1)*lenth,(i+1)*width,fill='white')
            elif mapifo[i][j]=='0':
                mapcanva.create_rectangle(j*lenth,i*width,(j+1)*lenth,(i+1)*width,fill='gray')
            elif mapifo[i][j]=='i':
                mapcanva.create_rectangle(j*lenth,i*width,(j+1)*lenth,(i+1)*width,fill='blue')
                inlet.change(i,j,inlet.pre)#入口
            else:
                mapcanva.create_rectangle(j*lenth,i*width,(j+1)*lenth,(i+1)*width,fill='green')
                outlet.change(i,j,outlet.pre)#出口
    player=mapcanva.create_oval((inlet.y+1/4)*lenth,(inlet.x+1/4)*width,(inlet.y+3/4)*lenth,(inlet.x+3/4)*width,fill='pink')#画布上显示玩家位置
    curpos=pos(inlet.x,inlet.y,None) #玩家当前位置
    bt1=Button(game,text='←',command=lambda: leftmove(mapifo,curpos,mapcanva,player))
    bt1.place(relx=0.8,rely=0.2,relwidth=0.05, relheight=0.05)
    bt2=Button(game,text='→',command=lambda: rightmove(mapifo,curpos,mapcanva,player))
    bt2.place(relx=0.9,rely=0.2,relwidth=0.05, relheight=0.05)
    bt3=Button(game,text='↑',command=lambda: upmove(mapifo,curpos,mapcanva,player))
    bt3.place(relx=0.85,rely=0.1,relwidth=0.05, relheight=0.05)
    bt4=Button(game,text='↓',command=lambda: downmove(mapifo,curpos,mapcanva,player))
    bt4.place(relx=0.85,rely=0.3,relwidth=0.05, relheight=0.05)
    bt5=Button(game,text='vs电脑玩家',command=lambda: pcpath(dif,mapifo))
    bt5.place(relx=0.82,rely=0.4,relwidth=0.1, relheight=0.1)
    bt6=Button(game,text='显示最短路径',command=lambda: pathlowcost(mapifo,mapcanva))
    bt6.place(relx=0.77,rely=0.55,relwidth=0.2, relheight=0.1)
    bt7=Button(game,text='是否存在通路',command=lambda: pathcheck(mapifo))
    bt7.place(relx=0.77,rely=0.7,relwidth=0.2, relheight=0.1)
    bt8=Button(game,text='保存该地图',command=lambda: mapsave(mapifo))
    bt8.place(relx=0.77,rely=0.85,relwidth=0.2, relheight=0.1)

def fileopen(file_path):
    filename = filedialog.askopenfile() #打开文件对话框
    if filename:#获取文件名
        file_path.set(filename.name)

def prepare(): #设置难度和选择地图函数
    mapset=Toplevel(root)
    mapset.title('迷宫设置')
    mapset.geometry('320x240')
    lb1 = Label(mapset,text='难度',font=('黑体',12,'bold'))
    lb1.place(relx=0.05,rely=0.2)
    dif=StringVar()#难度显示
    difchosen=ttk.Combobox(mapset,width=12,textvariable=dif)#下拉选择框
    difchosen['values']=('简单','适中','困难','高难')
    difchosen.place(relx=0.2,rely=0.2)
    lb2 = Label(mapset,text='地图',font=('黑体',12,'bold'))
    lb2.place(relx=0.05,rely=0.6)
    filefm = Frame(mapset)
    fopen = Button(filefm, text='...', command=lambda: fileopen(file_path))#文件对话框按钮
    fopen.pack(side=RIGHT)
    file_path = StringVar()#文件名显示
    entry = Entry(filefm, width=12, textvariable=file_path)
    entry.pack(side=LEFT)
    filefm.place(relx=0.2,rely=0.6)
    bt1=Button(mapset,text='确定',command=lambda: mapcreate(dif.get(),file_path.get(),mapset))
    bt1.place(relx=0.6,rely=0.2,relwidth=0.2, relheight=0.1)
    bt2=Button(mapset,text='取消',command=mapset.destroy)
    bt2.place(relx=0.6,rely=0.6,relwidth=0.2, relheight=0.1)

root = Tk() #主界面
root.title('迷宫游戏')
root.geometry('640x480')
photo=PhotoImage(file='./resource/backgroundimage.gif')#加载图片路径
imglb=Label(root,image=photo)
imglb.pack()
lb = Label(root,text='迷宫大作战',font=('黑体',16,'bold'),bg='white')
lb.place(relx=0.4,rely=0.04)
bt1=Button(root,text='开始游戏',command=prepare,bg='pink') #按钮
bt1.place(relx=0.47,rely=0.75,relwidth=0.1, relheight=0.06)
bt2=Button(root,text='退出',command=root.destroy,bg='pink') #按钮
bt2.place(relx=0.47,rely=0.85,relwidth=0.1, relheight=0.06)
random.seed(a=None) #随机数种子

root.mainloop()

