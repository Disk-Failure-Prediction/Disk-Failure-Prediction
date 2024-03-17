# OS:windows
# python3
# coding=utf-8
import os, re
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import namedtuple
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import roc_curve, auc, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score


def files_path(dir_name):
    """
    Reading all files' path in directory specified

    return:
    	files_path -- list of python

    """

    p1 = plt.imread('graphs\p1.png')
    plt.imshow(p1)
    plt.show()

    p1 = plt.imread('graphs\p2.png')
    plt.imshow(p1)
    plt.show()

    p1 = plt.imread('graphs\p3.png')
    plt.imshow(p1)
    plt.show()

    files_path = []
    for dirpath, _, filesname in os.walk(dir_name):
        for filename in filesname:
            files_path += [dirpath + "/" + filename]

    return files_path


#下面的注释也不能删除，都有实际用处  主要同于数据清洗、排序
#从原始数据集中取出某型号磁盘的某几个SMART属性
def data_filter(files_path, features, model):
    columns_specified = []
    for feature in features:
        columns_specified += ["smart_{0}_raw".format(feature)]
    # 制作好column内容
    columns_specified = ["date", "model", "failure"] + columns_specified
    # 建立预处理后数据的保存路径
    if not os.path.exists("data_preprocess/"):
        os.makedirs("data_preprocess/")
    for path in files_path:
        # 将/之前的路径删除，得到文件名
        t = re.split(r'/', path)
        # 读取csv文件
        datadf = pd.read_csv(path)
        # 选择对应型号的磁盘的索引
        data_model = datadf[datadf.model == model]
        # 将serial_number这一列作为索引
        data_model = data_model.set_index('serial_number')
        data_model = data_model[columns_specified]
        data_model.to_csv('data_preprocess/%s' % t[-1])

#本函数用于筛选出对应序列号的smart数值
def creat_dataset(nday, features):
    # 读预处理的数据
    filespath = files_path('data_preprocess/')
    # 存放column的内容
    columns_specified = []
    for feature in features:
        columns_specified += ["smart_{0}_raw".format(feature)]
    columns_specified = ["serial_number", "date", "model", "failure"] + columns_specified
    # 新建DataFrame型数据，并制定colums内容
    sample_data = pd.DataFrame(columns=columns_specified)
    # 挑选出所有failure=1的数据，并分别将前面10天failure由0改为1
    # -1表示倒序！！！
    # for i, path in enumerate(filespath[::-1]):
    #     df = pd.read_csv(path)
    #     Negative = df[df['failure'] == 1]
    #     # 连接：竖着连接，并集，不排序
    #     sample_data = pd.concat([sample_data, Negative], axis=0, join='outer', sort=False)
    #     if i < len(filespath) - nday:
    #         for j in range(nday - 1):
    #             df_next = pd.read_csv(filespath[i + j + 1])
    #             for s_num in np.array(Negative['serial_number']):
    #                 # 将failure值由0改为1
    #                 df_next.loc[df_next.serial_number == s_num, 'failure'] = 1
    #                 Negative_next = df_next[df_next.serial_number == s_num]
    #                 sample_data = pd.concat([sample_data, Negative_next], axis=0, join='outer', sort=False)
    # if not os.path.exists("Failure1/"):
    #     os.makedirs("Failure1/")
    # if not os.path.exists("Failure1_/"):
    #     os.makedirs("Failure1_/")
    # sample_data.to_csv('Failure1/Failure1Data.csv',index=False)
    # sample_data.to_csv('Failure1_/Failure1Data_.csv',index=False)
    #
    #
    #
    # 计算共多少failure=1的序列号，不重复
    dp_failure = pd.read_csv('Failure1/Failure1Data.csv')
    # dp_failure2=dp_failure['serial_number'].drop_duplicates(keep="first")
    dp_failure.drop_duplicates(subset=['serial_number'],keep="first",inplace=True)
    dp_failure.to_csv('Failure1/Failure1Data2.csv',index=False)
    # dp_failure_num = dp_failure.shape[0]
    # dp_failure_num2 = dp_failure2.shape[0]
    # print("Number of Failure1_Disk is %d. Repotation." % dp_failure_num)
    # print("Number of Failure1_Disk is %d. No repotation." % dp_failure_num2)

#     #从第一个文件中下采样failure0，使得failure0数量等于failure1数量
#     df = pd.read_csv('data_preprocess/2018-01-01.csv')
#     # 序列号去重
#     df['serial_number'].drop_duplicates(keep="first")
#     Positive_next = df[df['failure'] == 0].sample(n=dp_failure_num2)
#     Positive_next_serialnum = Positive_next["serial_number"]
#     print("Serial_number of Failure0_Disk is %s. No repotation." % Positive_next_serialnum)
#
#     #对所有failure0的数据下采样，选择相同的序列号
#     if not os.path.exists("Failure0/"):
#         os.makedirs("Failure0/")
#     for s_num in np.array(Positive_next_serialnum):
#         print("********************Failure0Sample************************************")
#         Sample_positive_cat = pd.DataFrame(columns=columns_specified)
#         for i, path in enumerate(filespath[::-1]):
#             df2 = pd.read_csv(path)
#             Sample_positive = df2[df2.serial_number == s_num]
#             Sample_positive_cat = pd.concat([Sample_positive_cat, Sample_positive], axis=0, join='outer', sort=False)
#             Sample_positive_cat.to_csv('Failure0/%s.csv' % s_num,index=False)
#     print("Sample is over~ ")
#
#
#     #生成Failure0_Sorted
#     if not os.path.exists("Failure0_Sorted/"):
#         os.makedirs("Failure0_Sorted/")
#     Failure0_path=files_path("Failure0/")
#     for path in Failure0_path:
#         # 将/之前的路径删除，得到文件名
#         t = re.split(r'/', path)
#         datadf = pd.read_csv(path)
#         datadf.sort_values(axis=0, ascending=True, by=['date']).to_csv('Failure0_Sorted/%s' % t[-1],index=False)
#         print("*********Failure0Sort**********")
#     print("Sorting is over~ ")
#
#
#
    #生成Failure1_Sorted
    # if not os.path.exists("Failure1_Sorted/"):
    #     os.makedirs("Failure1_Sorted/")
    # df_failure = pd.read_csv('Failure1/Failure1Data2.csv')
    # df_failure2 = df_failure['serial_number']
    # for s_num in np.array(df_failure2):
    #     print("*********Failure1Sort**********")
    #     Sample_positive_cat2 = pd.DataFrame(columns=columns_specified)
    #     for i, path in enumerate(filespath[::-1]):
    #         df = pd.read_csv(path)
    #         Sample_positive = df[df.serial_number == s_num]
    #         Sample_positive_cat2 = pd.concat([Sample_positive_cat2, Sample_positive], axis=0, join='outer', sort=False)
    #         Sample_positive_cat2.sort_values(axis=0, ascending=True, by=['date']).to_csv('Failure1_Sorted/%s.csv' % s_num,index=False)
    # print("Sample Failure1 is over~ ")
#######################################################################################################


    #去除最后一行，直接在原数据上进行
    #Failure1_Sorted数据
    df_failure = pd.read_csv('Failure1/Failure1Data2.csv')
    df_failure2 = df_failure['serial_number']
    for s_num in np.array(df_failure2):
        print("********************************************************")
        df_failure = pd.read_csv('Failure1_Sorted/%s.csv'%s_num)
        df_failure=df_failure[:-1]
        df_failure.to_csv('Failure1_Sorted/%s.csv'%s_num,index=False)

    #去除最后一行，直接在原数据上进行
    #Failure0_Sorted数据
    filespath = files_path('Failure0_Sorted/')
    for i, path in enumerate(filespath[::-1]):
        df_failure = pd.read_csv(path)
        df_failure=df_failure[:-1]
        df_failure.to_csv('%s'%path,index=False)
        #print("%s/n"%path)

#D:\DiskFailure\Disk-Failure-Prediction-master


def main():
    # 1.特征选择，型号选择
    features = [5, 9, 187, 188, 193, 194, 197, 198, 241, 242]
    model = "ST4000DM000"
    # 2.数据过滤:过滤出指定特征和型号
    filespath = files_path("data/")
    print(filespath)
    #data_filter(filespath, features, model)
    # 3.创建数据集：a.取raw数据b.故障回溯采正样本c.平衡数据集采负样本d.规范化输入
    creat_dataset(nday=10, features=features)



if __name__ == "__main__":
    main()
