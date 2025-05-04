import pandas as pd
import os
import numpy as np
import joblib
import random
b = []
file_list = os.listdir(r'D:\Forerunner\data\在建立西宁马尔可夫工况时导入的数据')
for i in file_list:
    if "gps" in i:
        b.append(i)

# 检验开头和结尾是否为0和合并
a = 1
df_kong = pd.DataFrame()
for i in range(0, len(b)):
    df = pd.read_csv(r'D:\Forerunner\data\在建立西宁马尔可夫工况时导入的数据' + '\\' + b[i])
    df['wenjian'] = a
    a = a + 1
    print(df['SPEED'][0])
    print(df['SPEED'][len(df['SPEED']) - 1])
    print(i)
    df_kong = df_kong.append(df)

##检验是否有空值并重置index
# df_kong1=df_kong[df_kong['SPEED'].isnull()]

df_kong = df_kong.reset_index()
del df_kong['index']

df_kong['acc'] = df_kong['SPEED'].diff(1) / 3.6
df_kong = df_kong.fillna(0)
df_kong['acc'].describe()
# df_kong['acc_new']=round(df_kong['acc']/0.01)*0.01
df_kong['acc_new'] = round(df_kong['acc'], 2)
df_kong['speed_new'] = df_kong['SPEED'] / 3.6
df_kong['speed_new'] = round(df_kong['speed_new'], 1)
df_kong['height_new'] = round(df_kong['HEIGHT'], 1)

df_kongg = df_kong.astype({'speed_new': 'str', 'acc_new': 'str', 'height_new': 'str'})
df_kongg["speed_acc_height"] = df_kongg["speed_new"] + "_" + df_kongg['acc_new'] + "_" + df_kongg['height_new']

from collections import defaultdict
from collections import Counter

tra = df_kongg['speed_acc_height'].tolist()
start_count = 0
token_count = 0
vocab_count = 0
# 统计v-a-h状态出现的次数
unigram_counts = Counter()
for word in tra[:]:
    unigram_counts[word] += 1

bigram_counts = defaultdict(Counter)
context = defaultdict(Counter)
bigram_list = zip(tra[:-1], tra[1:])
for bigram in bigram_list:
    bigram_counts[bigram[0]][bigram[1]] += 1
    context[bigram[1]][bigram[0]] += 1
token_count = sum(unigram_counts.values())
vocab_count = len(unigram_counts.keys())

# 创建新的dataframe
df_shaxuan = pd.DataFrame()
df_shaxuan["ID"] = list(bigram_counts.keys())

keys_list = []
for i in range(len(df_shaxuan["ID"])):
    keys = list(bigram_counts[df_shaxuan["ID"][i]].keys())
    keys_list.append(keys)

df_shaxuan["keys"] = keys_list

values_list = []
for i in range(len(df_shaxuan["ID"])):
    values = [(np.array(list(bigram_counts[df_shaxuan["ID"][i]].values())) / sum(
        bigram_counts[df_shaxuan["ID"][i]].values())).tolist()]
    values_list.append(values)

df_shaxuan["values"] = values_list

def continue_judgement(speed_list):
    testkong1 = pd.DataFrame(speed_list)
    testkong1.columns = ["SPEED"]
    testkong2 = testkong1["SPEED"].str.split("_", expand=True)
    testspeed_list_pre = testkong2[0].tolist()
    testheight_list_pre = testkong2[2].tolist()
    ##字符转换成数字
    testspeed_list_real = list(map(float, testspeed_list_pre))
    testheight_list_real = list(map(float, testheight_list_pre))
    testspeed_height_real = pd.DataFrame({'SPEED': testspeed_list_real, 'HEIGHT': testheight_list_real})
    testspeed_height_real.index = range(0, len(testspeed_height_real))
    if testspeed_height_real["SPEED"].max() <= 25:
        if testspeed_height_real[testspeed_height_real["SPEED"] == 0].count()[0] <= 270:
            return True
    return False


def process(df_shaxuan):
    k = 1
    df_real_speed = pd.DataFrame()
    while len(df_real_speed.columns) < 8:

        speed_list = ['0.0_0.0_2222']
        c = '0.0_0.0_2222'
        j = 1
        for i in range(1799):
            d = np.random.choice(df_shaxuan[df_shaxuan["ID"] == c]["keys"].tolist()[0],
                                 p=df_shaxuan[df_shaxuan["ID"] == c]["values"].tolist()[0][0])
            c = d
            speed_list.append(d)
            j += 1
            if j == 900:
                test = continue_judgement(speed_list)
                if not test:
                    print("在900秒的时候中断了！")
                    break
        if test:
            df_kong1 = pd.DataFrame(speed_list)
            df_kong1.columns = ["SPEED"]
            df_kong2 = df_kong1["SPEED"].str.split("_", expand=True)
            speed_list_pre = df_kong2[0].tolist()
            height_list_pre = df_kong2[2].tolist()
            ##字符转换成数字
            speed_list_real = list(map(float, speed_list_pre))
            height_list_real = list(map(float, height_list_pre))
            speed_height_real = pd.DataFrame({'SPEED': speed_list_real, 'HEIGHT': height_list_real})
            speed_height_real.index = range(0, len(speed_height_real))

            if True:  # 第一个条件总的停止值小于270

                df_kong3 = pd.DataFrame(speed_height_real)
                if True:  # 第二个条件。速度等于0，终末。
                    df_kong4 = pd.DataFrame(df_kong3)
                    if True:  # 第三个条件，最大值小于25
                        df_kong5 = pd.DataFrame(df_kong4)
                        df_kong5 = df_kong5.fillna(0)
                        df_kong6 = pd.DataFrame(df_kong5)
                        speed_list_real1 = df_kong6["SPEED"]
                        speed_list_real1 = speed_list_real1.tolist()
                        height_list_real1 = df_kong6["HEIGHT"]
                        height_list_real1 = height_list_real1.tolist()
                        df_real_speed['s' + str(k)] = speed_list_real1
                        df_real_speed['h' + str(k)] = height_list_real1
                        print("一个成功的来了！")
                        k += 1
                        df_real_speed.to_csv(rf"D:\桌面\新建文件夹\1{random.randint(1, 100000)}.csv", encoding="gbk")
        else:
            continue
    return df_real_speed


if __name__ == "__main__":
    num_cores = joblib.cpu_count()
    results = joblib.Parallel(n_jobs=16, backend="loky", prefer="processes")(
        joblib.delayed(process)(df_shaxuan) for i in range(num_cores)
    )
    for result in results:
        print(result)










