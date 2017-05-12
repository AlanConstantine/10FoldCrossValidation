# -*- coding: utf-8 -*-
# @Date    : 2017-05-11 21:24:50
# @Author  : Alan Lau (rlalan@outlook.com)
# @Version : Python3.5

from fwalker import fun
from bfile import buildfile as bf
from random import shuffle
import numpy as np
import shutil
import os


def buildfile(output_path):
    for i in range(1, 10+1):
        # 循环新建编号1-10的文件夹，用于存放train和test文件夹
        file_num = bf('%s\\%d' % (output_path, i))
        # 在每个编号文件夹下新建train文件夹，用于存放90%的训练数据
        train_file = bf('%s\\train' % file_num)
        # 在每个编号文件夹下新建test文件夹，用于存放10%的训练数据
        test_file = bf('%s\\test' % file_num)
    print('Data storage has been bulit!')
    return output_path


def split_ten(files):
    file_len = len(files)  # 获取文件总数
    shuffle(files)  # 随机打乱文件路径列表的顺序，即使python的随机是伪随机
    data_storage = []  # 初始化一个列表，用来接收分划分好的文件路径
    remainder = file_len % 10  # 判断文件数量能否直接被10整除
    if remainder == 0:  # 如果可以整除，直接将数据切成10组
        np_files = np.array(files)  # 将文件路径列表转换成numpy
        data_storage = np_files.reshape(10, -1)  # 利用numpy的reshape来将文件路径切分为10组
        # 比如说现在有20个文件路径
        # reshape()后得到的结果为2、2、2、2、2、2、2、2、2、2，即共十份、每份包含2个文件路径。
        return data_storage
    else:  # 否则，则先切开余数部分的文件
        np_files = np.array(files[:-1*remainder])  # 切开余数部分的文件，使文件数量保证能够被10整除
        data_storage_ten = np_files.reshape(10, -1)  # 同样利用上面的方法使用numpy切分10组文件
        # 获取余数部分的文件列表，遍历列表，尽可能的将多余的文件分散在10组文件中，而不是直接加入到一个文件中
        remainder_files = (
            np.array(files[-1*remainder:])).reshape(remainder, -1)  # 使用reshape切分问一份一组
        for i in range(0, len(remainder_files)):
            ech_dst = data_storage_ten[i]
            ech_rf = remainder_files[i]
            # 将取出来的余数内的路径分别加入到已经均分好的10份的前remainder个数据当中，比如说现在有24份文件，
            # 将24拆份拆分成一个能被10整除的数和一个余数，即这里拆分成20和4，我们首先将拆出来的20份文件均分10份，
            # 即每份有2个文件路径，然后，再将剩下后面的4个文件路径，尽可能的放入到刚刚均分好的10份数据中。
            # 因此最终拆分的结果共有十份，每份数量分别为：3、3、3、3、2、2、2、2、2、2。
            data_storage.append(np.concatenate((ech_dst, ech_rf)))
        for j in range(remainder, len(data_storage_ten)):
            # 将将剩下的没有被余数部分加入的份加入到data_storage中
            data_storage.append(data_storage_ten[j])
        return np.array(data_storage)


def group_data(data_storage, output_path):
    for i in range(0, len(data_storage)):
        ech_path = '%s\\%d' % (output_path, i+1)  # 构造每一份需要写入的路径
        ech_train_path = '%s\\train' % ech_path
        ech_test_path = '%s\\test' % ech_path
        test_paths = data_storage[i]
        move_file(test_paths, ech_test_path)
        train_paths = np.concatenate(([data_storage[:i], data_storage[i+1:]]))
        # 将剩下的训练部分加入到train_paths中，并且降维
        train_paths = np.concatenate((train_paths))  # 再次降维，使其变成1维
        move_file(train_paths, ech_train_path)
        num = i+1
        print('No.%d is over!' % num)


def move_file(old_paths, new_path):
    for old_path in old_paths:
        shutil.copy2(old_path, new_path)
        flag_name = '_'.join(old_path.split('\\')[-2:])
        old_name = '%s\\%s' % (new_path, old_path.split('\\')[-1])
        new_name = '%s\\%s' % (new_path, flag_name)
        os.rename(old_name, new_name)


def main():
    file_path = r'..\data\data_of_movie'
    # file_path = r'..\data\test'
    output_path = r'..\data\tenTimesTraining'
    files = fun(file_path)
    # output_path = buildfile(output_path)
    data_storage = split_ten(files)
    group_data(data_storage, output_path)


if __name__ == '__main__':
    main()
