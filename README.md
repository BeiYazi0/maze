## maze

python项目 迷宫游戏

## 主界面

背景图片可自行修改，但必须是gif文件，文件名为“backgroundimage.gif”，图片大小为640x480。

![image](https://github.com/BeiYazi0/maze/blob/main/test/main.PNG)

## 设置界面

1.难度自选，根据难度不同，难度系数也有所不同，难度系数一定程度上代表了电脑玩家每次行动选择当前位置下最优路径指向的下一位置的概率。难度系数在0.35-0.95之间，如选择高难，则电脑玩家有95%的可能选择当前位置下的最优的下一位置，5%的可能选择其它位置。

2.地图可以直接由文件导入，若不选择文件则随机制造一个迷宫。地图文件规范如下，用'1'标记能前往的位置，用'0'标记不能前往的位置，用'i'标记入口，用'o'标记出口。

![image](https://github.com/BeiYazi0/maze/blob/main/test/set.PNG)

## 游戏界面

1.四个方向键代表四个方向。

2.“vs电脑玩家”和“显示最短路径”两个按钮的功能只有在完成游戏后才有效。

3.由于玩家自己选择的地图可能出现没有通路的问题，所有增加了一个按钮用于判断，随机迷宫已经处理过了，没有这样的问题。

4.玩家可以将自己喜欢的迷宫保存起来备用，起文件名时禁止使用< > / \ | : " * ?这些字符，不需要添加后缀，迷宫文件后缀一律为txt。

![image](https://github.com/BeiYazi0/maze/blob/main/test/game.PNG)

## 存在的问题

1.所有界面除了主界面外都是主界面的子窗口，看样子好像能创建多个迷宫游戏的界面，但不要这么做，代码中计步数或控制游戏的变量有限，打开多个迷宫可能会出大问题，请先关闭当前的迷宫界面，再点击开始游戏打开新的迷宫界面。

2.由于随机迷宫比较大，不建议选择简单模式后使用随机迷宫，可能卡住，也可能只是我电脑的问题。

3.事实上电脑玩家使用的策略或许只能算一个，每次行动前以自身位置发起广度优先搜索，找出最短路径，不同的难度只是人为地给它一个“干扰”，让它不一定选中当前位置下的下一个最优位置，难度不同干扰强度不同。
