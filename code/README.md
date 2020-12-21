## 文件介绍
该目录下 simple-HRNet-master 是用大模型 HRNet 产生关键点数据用于之后小模型的训练。

Ultralight-SimplePose-master 是小模型，在里面存放了训练代码，和将大模型得到的关键点数据转换为 coco 格式的代码。

Ultralight-SimplePose-master 目录下 convet2coco(modify).py 用于将关键点数据转换为 coco 格式，train_simple_pose.py 用于训练模型。

simple-HRNet-master 目录下 vedio_batch_test 用于批量生成关键点检测数据，并保存每一帧的图片和相应的关键点数据（.asv文件）。
