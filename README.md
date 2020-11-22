# Attitude-Recognition-Datasets
 侧面姿态识别关键点数据集
 
 这里的 output1 是使用 Simple_HRNet-master 得到的。其中，frame_output 是每一帧的图片，view_output 是加上关键点和骨干可视化后的效果，然后 output.csv 是关键点数据，但目前数据有点对不上。
 
 ## 目前工作进度：
   1.simple-HRNet-master 和 Ultralight-SimplePose 都已经调通，并且修改代码输出可视化效果和关键点数据
 
 ## 目前的主要问题就是：
 图片上的人物之间很多有重叠，不够简洁，比较难提取出想要的某个人的姿态关键点。所有就没法做出比较好的训练集。
 
 ## 解决方法：
   1.在 coco 数据集里挑选一些简洁一点的人物侧面图片作为一部分训练集
   2.将某些原本的深蹲，仰卧起坐等图片，选取一些人比较少的进行截取
   3.调高 yolov3 的置信度（目前不太有用，因为只要程序检测到某个人物框，该人物框的置信度就会比较高（95%左右），即使这个人物并不是我们需要的）

coco 数据集里较好的侧面图：

![image](https://github.com/LQQQQQQQQQQ/Attitude-Recognition-Datasets/blob/main/data/2.jpg)

simple-HRNet-master 测试效果：

![image](https://github.com/LQQQQQQQQQQ/Attitude-Recognition-Datasets/blob/main/data/out.jpg)

Ultralight-SimplePose 测试效果：

![image](https://github.com/LQQQQQQQQQQ/Attitude-Recognition-Datasets/blob/main/data/myplot.png)
