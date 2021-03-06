#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math, random, os
from exl import readexcel

'''
    4组训练样本
    输入层: 4 节点
    隐藏层: 7 节点 + 1 阈值节点(输出为1, 权值为bj)
    输出层: 1 节点

    前向传输:
        第一层传输: for A in examples for j in range(0,7) B[j] = 0 for i in range(0,4) B[j] += A[i] * A[j][i]
        第二层传输: 
    反向传播:
        隐藏到输出: for i in range(0,7) for j in range(0,1) deltw = (y-t) * y * (1-y) * output(y)

'''

# sigmoid(x) = 1/(1+exp(-x)), sigmoid'(x) = sigmoid(x)(1 - sigmoid(x))
# th(x) = (exp(x) - exp(-x)/(exp(x) + exp(-x)), th'(x) = 1 - th(x) * th(x)
def act_function(x, z):
    if z == "sigmoid" :
        return 1/(1 + math.exp(-x))
    elif z == "th":
        return (math.exp(x) - math.exp(-x))/(math.exp(x) + math.exp(-x))
    elif z == "linear":
        return x
    else:
        raise ValueError('invalid value: %s' % z)

def act_function_derivatives(y, z = "sigmoid" ):
    if z == "sigmoid":
        return y * (1 - y)
    elif z == "th":
        return 1 - y * y
    elif z == "linear":
        return 1
    else:
        raise ValueError('invalid value: %s' % z)

class BP:
    
    # _input_examples_values
    # _output_examples_values
    # _hiding_nodes
    # _output_nodes
    # _input_w
    # _output_w
    # _lamda
    
    def __init__(self, input_examples_values = None, output_examples_values = None, examples = None, hiding_nodes_number = 8, lam = 0.3):
        # examples[4][0][4] [4][1][1]
        # self.examples = examples
        if examples:
            # _input_examples_nodes[4][4], 保存数据集中的所有输入数据的值
            self._input_examples_values = [p[0] for p in examples]
            # _output_examples_values[4][1], 保存数据集中的所有输出数据的值
            self._output_examples_values = [p[1] for p in examples]
            # 训练样本数
            train_num = len(examples)
        elif input_examples_values != None and output_examples_values != None:
            # _input_examples_nodes[4][4], 保存输入数据集中的所有数据的值
            self._input_examples_values = input_examples_values
            # _output_examples_values[4][1], 保存输出数据集中的所有数据的值
            self._output_examples_values = output_examples_values
            # 训练样本数
            train_num = len(input_examples_values)
        else:
            raise ValueError('没有输入 input_examples_values, output_examples_values 或 examples')
       
        # _hiding_nodes[4][8], 用于保存bp神经网络对于每个输入的隐藏层的值
        self._hiding_nodes = [[(i+1)//hiding_nodes_number for i in range(hiding_nodes_number)] for j in range(train_num)]
        # _output_nodes[4][1], 用于保存bp神经网络的输出值
        self._output_nodes = [[0] * len(self._output_examples_values[0]) for j in range(train_num)]
        
        # 输入层 到 隐藏层 权值 w[7][4], w[7][4] * a[4][1] = h[7][1]
        self._input_w = [[random.random() for j in range(len(self._input_examples_values[0]))] for i in range(hiding_nodes_number - 1)]
        # 隐藏层 到 输出层 权值 w[1][7], w[1][7] * h[7][1] = o[1][1]
        self._output_w =  [[random.random() for j in range(hiding_nodes_number)] for i in range(len(self._output_examples_values[0]))]
        # 设置误差导数更新步长
        self._lamda = lam

    # 根据 权值矩阵 和 输入数据 更新 BP神经网络的 输出层数据
    def Forward_propagation(self, _input_eg_values = None ):
        if _input_eg_values == None:
            _input_examples_values = self._input_examples_values
        else:
            _input_examples_values = _input_eg_values
        # 第 m 个训练样本
        for m in range(len(_input_examples_values)):
            # 输入层 到 隐藏层 加权后使用激活函数 sigmoid(x) = 1 / (1+exp(-x))
            # 第 i 个隐藏层节点
            for i in range(len(self._hiding_nodes[0])-1):
                self._hiding_nodes[m][i] = 0
                # 第 j 个输入层节点
                for j in range(len(_input_examples_values[0])):
                    self._hiding_nodes[m][i] += self._input_w[i][j] * _input_examples_values[m][j]
                self._hiding_nodes[m][i] = act_function(self._hiding_nodes[m][i], "sigmoid")
            # 隐藏层 到 输出层 加权后使用激活函数 f(x) = x
            # 第 i 个输出层节点
            for i in range(len(self._output_examples_values[0])):
                self._output_nodes[m][i] = 0
                # 第 j 个隐藏层节点
                for j in range(len(self._hiding_nodes[0])):
                    self._output_nodes[m][i] += self._output_w[i][j] * self._hiding_nodes[m][j]
                self._output_nodes[m][i] = act_function(self._output_nodes[m][i], "linear")

    def Backward_propagation(self):
        delta_w_out = [[0 for j in range(len(self._hiding_nodes[0]))] for i in range(len(self._output_examples_values[0]))]
        delta_w_in = [[0 for j in range(len(self._input_examples_values[0]))] for i in range(len(self._hiding_nodes[0])-1)]
        # 第 m 个训练样本
        for m in range(len(self._input_examples_values)):
            # 隐藏层 到 输出层 误差导数 delta_w[i][j] = -lamda * x[i] * (y[j] - t[j]) * y[j] * (1 - y[j])
            for i in range(len(self._output_examples_values[0])):
                for j in range(len(self._hiding_nodes[0])):
                    delta_w_out[i][j] += self._hiding_nodes[m][j] * (self._output_nodes[m][i] - self._output_examples_values[m][i]) * act_function_derivatives(self._output_nodes[m][i], z = "linear")
            # 输入层 到 隐藏层 误差导数
            for i in range(len(self._hiding_nodes[0])-1):
                for j in range(len(self._input_examples_values[0])):
                    for k in range(len(self._output_examples_values[0])):
                        delta_w_in[i][j] += self._input_examples_values[m][j] * (self._output_nodes[m][k] - self._output_examples_values[m][k]) * act_function_derivatives(self._output_nodes[m][k], z = "linear") * self._output_w[k][i] * act_function_derivatives(self._hiding_nodes[m][i], "sigmoid")
        # 更新每一个权值
        for i in range(len(self._output_examples_values[0])):
            for j in range(len(self._hiding_nodes[0])):
                self._output_w[i][j] = self._output_w[i][j] - self._lamda * delta_w_out[i][j] / (m + 1)
        for i in range(len(self._hiding_nodes[0])-1):
            for j in range(len(self._input_examples_values[0])):
                self._input_w[i][j] = self._input_w[i][j] - self._lamda * delta_w_in[i][j] / (m + 1)
            
    def Squared_error(self, _output_eg_values = None, _out_nodes = None):
        if _output_eg_values != None and _out_nodes != None:
            _output_examples_values = _output_eg_values
            _output_nodes = _out_nodes
        elif _output_eg_values != None and _out_nodes == None:
            _output_examples_values = _output_eg_values
            _output_nodes = self._output_nodes
        else:
            _output_examples_values = self._output_examples_values
            _output_nodes = self._output_nodes
        e = 0
        # BP网络输出 和 训练集中输出值 的范数之差的平方，后将所有训练集中的样本的误差累加到一起
        for m in range(len(_output_examples_values)):
            o = 0
            ov = 0
            for value in _output_examples_values[m]:
                o += value * value
            for value in _output_nodes[m]:
                ov += value * value
            o = math.sqrt(o)
            ov = math.sqrt(ov)
            e += (o - ov) * (o - ov)
        return e/(m+1)
            
            
    def train(self, time = 1000, print_state = False):
        self.Forward_propagation()
        print("训练次数: Error")
        for i in range(time):
            # error_before = self.Squared_error()
            self.Backward_propagation()
            self.Forward_propagation()
            error_after = self.Squared_error()
            if (i + 1) % 50 == 0:
                print(i + 1, ":", error_after)
        if print_state:
            print("example input\t actual output\t predicted output")
            for i in range(len(self._input_examples_values)):
                print(self._input_examples_values[i], self._output_examples_values[i], self._output_nodes[i])
            
    def test(self, input_test_values = None, output_test_values = None, test_eg = None, print_state = False):
        if test_eg:
            _input_examples_values = [p[0] for p in test_eg]
            _output_examples_values = [p[1] for p in test_eg]
            test_num = len(test_eg)
        elif input_test_values != None and output_test_values != None:
            _input_examples_values = input_test_values
            _output_examples_values = output_test_values
            test_num = len(input_test_values)
        else:
            raise ValueError('没有输入 input_test_values, output_test_values 或 test_eg')
        
        self.Forward_propagation(_input_examples_values)
        error = self.Squared_error(_output_eg_values = _output_examples_values)
        print("测试数据集 Error:", error)
        if print_state:
            print("test input\t actual output\t predicted output")
            for i in range(test_num):
                print(_input_examples_values[i], _output_examples_values[i], self._output_nodes[i])

def import_data():
    dir = [x for x in os.listdir('.') if os.path.isdir(x) or '.xls' in os.path.splitext(x)[1]]
    print(dir)
    filebox = "./" + input("输入导入的文件/文件所在文件夹")
    while os.path.isdir(filebox):
        print([x for x in os.listdir(filebox) if os.path.isdir(x) or '.xls' in os.path.splitext(x)[1]])
        filebox += "/"+input("输入导入的文件/文件所在文件夹")
    if os.path.isfile(filebox):
        return readexcel(filebox)

def main():
    examples_1 = [
                  [[1, -1, 0, 0], [1,]],
                  [[0, 1, 0, -1], [-1,]],
                  [[1, 1, -1, 0], [2,]],
                  [[-1, -1, -1, -1], [-2,]],
                  ]
    test_1 = None

    examples = examples_1

    '''
    l_in_1 = readexcel("/Users/Welkin/Documents/人工智能/BackwardPropagation/data3/P.xlsx")
    l_out_2 = readexcel("/Users/Welkin/Documents/人工智能/BackwardPropagation/data3/T.xlsx")
    print("训练集样本数：", len(l_in_1), len(l_out_2))
    train_num = -3
    bp = BP(input_examples_values = l_in_1[:train_num], output_examples_values = l_out_2[:train_num], hiding_nodes_number = 8)
                                                                                                
    #bp = BP(input_examples_values = l_in_eg, output_examples_values = l_out_eg)
    bp.train(time = 1000, print_state = False)
    
    bp.test(l_in_1[train_num:], l_out_2[train_num:], print_state = False)

    # bp.test(l_in_test, l_out_test)
    '''
    print("import 输入数据集")
    l_in = import_data()
    print("import 输出数据集")
    l_out = import_data()
    
    
    print("训练集样本数：", len(l_in), len(l_out))
    
    if len(l_in) < 5:
    raise ValueError("数据集样本太少")
    
    if len(l_in) != len(l_out):
    raise ValueError("数据集样本数不匹配")
    
    
    while True:
    train_num = int(input("输入训练样本数（其他样本用于测试）："))
    if abs(train_num) < len(l_in) :
    break
    else:
    print("输入有误, len(l_in) = ", len(l_in))
    
    l_in_eg = l_in[:train_num]
    l_out_eg = l_out[:train_num]
    l_in_test = l_in[train_num:]
    l_out_test = l_out[train_num:]
    bp = BP(input_examples_values = l_in_eg, output_examples_values = l_out_eg)
    bp.train(time = 1000, print_state = False)
    bp.test(l_in_test, l_out_test)


if __name__=="__main__":
    main()


