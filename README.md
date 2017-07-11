<h1>BackPropagation</h1>

引知乎YJango回复（关于反向传播算法）：所有神经网络的反向传播算法都是一样的。有基础的微积分知识（到链式法则，也就是函数内套函数的导数的求法）。而神经网络的话，是求将其他维度的变量看成常量的偏导数。如果微积分的知识不牢固，请看斯坦福strang老爷子的微积分重点 http://open.163.com/special/opencourse/weijifen.html 。如果没有问题，那看这篇 http://colah.github.io/posts/2015-08-Backprop/ 。关于实践部分（不用tensorflow自带的update方式），先自己在纸上推出导数，再在pytorch上用自带的自动求导验证自己的结果，加深体会。


！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

运行方法：
先将运行目录设置为当前目录，然后在命令行执行：python3 BP3_x_x.py 或 ./BP3_x_x.py
使用要求：
先将文件中import的几个包都通过 pip3 install xxxxx 指令安装好，然后按照上面的运行方法运行

！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

改进方向：
1. 引入模拟退火算法，用于跳出局部最小值



<h2>Version:</h2>

<h3>BP3.0.1:</h3>

更新：
1. 修复隐藏层节点更新的bug

已知算法缺陷：
1. 使用th激活函数时，隐藏层节点非常容易进入饱和区，导致梯度消失
2. 当矩阵中元素趋近于0时，numpy会将元素变为nan



<h3>BP3.0.0:</h3> (将应用于BP神经网络的数据全部部署为numpy矩阵，计算速度提升)

更新：
1. 引用bplib_3包





BP2.5 beta:

更新：
1. 更换 数据存储方式，用np.array替换list
2. 更改权值矩阵初始值，使用Xavier初始化方法
3. 更改附加动量因子的权值调节公式，delta_w = (1 - kc) * lamda * derivative_w + kc * lamda * derivative_w_old


BP2.6:

更新：
1. 更改附加动量因子的权值调节公式，delta_w = (1 - kc) * lamda * derivative_w + kc * lamda * derivative_w_old
2. 将引用的.py文件移至bplib_2文件夹中



BP2.5.1:

更新：
1. 更改权值矩阵初始值，使用Xavier初始化方法



BP2.5:

更新：
1. 增加一个归一化方法，x = (x - min)/(max - min)
2. 最大最小值归一化方法在测试中表现很差，不适合用于数据归一化



BP2.4:

更新：
1. 增加一个终止条件，当error < 10^-6时，可以终止，目前随机训练的误差终止还不完善
2. 训练函数现在会返回迭代次数
3. BP初始化函数增加属性，现在可以设置 隐藏层激活函数、输出层激活函数



BP2.3:

更新：
1. 随机和批量训练都加入了梯度计算
2. 缩减代码，将几个show函数放入show.py中



BP2.2:

更新：
1. 增加gradient梯度计算，每次训练后计算输出层对隐藏层权值的梯度
2. 增加梯度图像显示，纵坐标为对数坐标轴



BP2.1:

更新：
1. 缩减代码，删除了几个没有用的函数
2. 更新了随机梯度下降算法，现在每次训练单个数据时会将学习率除以一个系数，这个系数默认为样本数量
3. 更新了随机梯度下降算法的训练方式，现在可以在每次随机训练时同时查看测试误差
4. 可以选择使用批量梯度下降算法或者随机梯度下降算法



BP2.0 (有动量梯度下降法):

更新：
1. 更新梯度下降算法，现在每次权值会同时将 当前误差导数 与 上一次的误差导数 乘系数后相加
2. BP神经网络训练后，计算 网络输出 和 实际输出 的回归曲线方程(y = k * x + b)和随机误差(R)，并分别画出训练集、测试集、全样本集的 散点图和线性回归曲线
3. 增加图例
4. MSE图像，纵坐标（MSE坐标）改用对数坐标系表示
5. 更新了训练集和测试集的选取方式，现在采用随机在样本集中选择的方式

目前只实现了 批量梯度下降算法 的显示



BP1.5.0 (标准梯度下降法，稳定版):

更新：
1. 批量梯度下降和随机梯度下降分开
2. 混合训练：混合批量训练和测试两个函数，每次迭代训练后同时记录 训练集 和 测试集 的输出MSE误差
3. 将两个误差同时显示在一张图像上并展示，训练误差用红色线条表示，测试误差用绿色线条表示



BP1.4:

更新：
1. 每次迭代的误差以图像形式显示，但是图像的坐标轴不能以指数形式展示



BP1.3:

更新：
1. 输入、输出数据集归一化后再传入BP神经网络，归一化函数:x = (x - mu) / sigma, mu为均值，sigma为标准差
2. 误差计算时先将归一化的数据反归一化，再计算输出误差
3. 将main() 和测试用的 demo() 分开，main()中通过命令行选择导入的Excel文件



BP1.2:

更新：
1. 可以通过Excel文件导入训练集数据
2. 可以控制训练结束后显示/不显示样本集和神经网络输出



BP1.1:
依旧采用固定隐藏层中神经节点个数的方式

更新：
1. 样本集使用三维列表代替字典
eg = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]
2. 采用批量梯度下降法，每次反向更新权值时使用样本集中全部样本的误差来计算
3. 可以自己选择激活函数，增加了一个 th(x) 函数，函数范围为 (-1,1)
4. 更改了BP类的数据结构，现在初始化BP类的实例时必须传入一个训练集
5. BP类内增加了训练函数，默认训练1000次传入的训练集中的数据
6. 将误差计算函数内置到BP类中，默认计算传入的训练集的输出和神经网络输出间的误差
7. 在BP类中增加测试函数，可以传入测试数据集进行测试，可以打印此神经网络对测试集的误差，和测试集的输出结果



BP1.0:

三层神经网络，隐藏层中7个神经节点+1个阈值节点

隐藏层激活函数：只设计了一种，直接写进BP反向更新权值的函数中了 sigmoid(x) = 1/(1-exp(-x))

输出层激活函数：f(x) = x

初始权值：随机生成 0~1 之间的权值

对数据集没有采用归一化处理

训练模式：每次输入一个训练集中的数据，更新权值后再输入下一个数据进行训练，直到训练集中数据全部被训练过，然后循环 N 次

缺点：
1. 每次训练一组训练集中的数据后，权值会更改 m 次，而且每次权值的更改都是按照当前训练的数据的最优方向进行的修改，对整体数据集训练效果不友好，容易陷入局部最小值
2. 误差计算有问题，对于每个训练集中的数据，训练之后误差都会减小，但是当将这些对权值的修改累加到一起后，再次训练到这个数据时，其误差又增大到上次训练这个数据时的误差附近。可以得出的结论是，对数据集中的数据单独训练的结果会使其他数据的误差增大，这种训练方式不能得到全局最优误差下降曲线
3. 对于一组含有4个样本的训练集进行训练，
examples_1 = {(1, -1, 0, 0) : [1,]
            , (0, 1, 0, -1) : [-1,]
            , (1, 1, -1, 0) : [2,]
            , (-1, -1, -1, -1) : [-2,]}
对于1000次反向传播修改权值训练后，BP网络成功记住这些样本数据的的概率大约为 70% (11次试验中，1次因为浮点数越界而失败，7次达到epsilon<0.001的准确度，3次陷入局部最优值)，其概率与随机生成的初始权值矩阵中的数据有关
4. 对于随机产生的进行分类测试的样本集进行训练，
    A = [(random.random(), random.random()) for y in range(0,20)]
    B = [(-random.random(), random.random()) for y in range(0,20)]
    C = [(-random.random(), -random.random()) for y in range(0,20)]
    D = [(random.random(), -random.random()) for y in range(0,20)]
将 AB, CD分为两组输入数据，输出值分别为 -1 和 1，在1000次训练后，BP网络不能成功将这些数据进行分类(试验次数>5，0次成功)

针对以上试验结果，可以认为：隐藏层激活函数为 sigmoid，输出层激活函数为 线性函数 的单次训练模式 的BP神经网络，适用于回归(拟合)问题(>70%)，但不适用于分类问题
