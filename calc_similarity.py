import sys
import time
import re
import argparse
import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import urlparse
from collections import OrderedDict


# コマンドライン引数についての設定

parser = argparse.ArgumentParser()
parser.add_argument('userurl_first', type=str,
                    help='inputfile1 (first half period): each record includes userid and url (bookmarked)')
parser.add_argument('userurl_second', type=str,
                    help='inputfile2 (second half period): same to inputfile1 but period is different')
parser.add_argument('-m', '--method', type=str, required=True,
                    help='select method to calculate the similarity between sets (jaccard, dice, simpson, intersection)')
args = parser.parse_args()

# 集合間の類似度を求める関数

def jaccard(set_a, set_b):
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union

def dice(set_a, set_b):
    intersection = len(set_a & set_b)
    return 2*intersection / (len(set_a) + len(set_b))

def simpson(set_a, set_b):
    intersection = len(set_a & set_b)
    return intersection / min(len(set_a), len(set_b))

# 共通要素の数を数える関数（上３つと同様に集合間の類似度合を測る）

def count_intersection(set_a, set_b):
    return len(set_a & set_b)

# 辞書のkey名を変更する関数

# def change_dict_key(d, old_key, new_key, default_value=None):
#     d[new_key] = d.pop(old_key, default_value)

# 前半期間のファイルを読み込んでユーザをkey、そのユーザがアクセスしたURLの集合をvalueとする辞書の作成

users_first = set()
urls_first = set()
user_urls_first = {}
# user_number = {}
# i = 1
with open(args.userurl_first, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.rstrip()
        if line == '':
            continue
        user, url = line.split(':', 1)
        users_first.add(user)
        #urls_first.add(url)
        #ドメインベースでの解析
        urls_first.add(urlparse(url).netloc)
        #userがキーに存在していない時、空集合を作成
        if user not in user_urls_first:
            #辞書の作成
            user_urls_first[user] = {url} # ランダム
            # user_number[i] = user # ソート済
            # i = i + 1
        else:
            user_urls_first[user].add(url)

# 後半期間のファイルを読み込んでユーザをkey、そのユーザがアクセスしたURLの集合をvalueとする辞書の作成

users_second = set()
urls_second = set()
user_urls_second = {}
with open(args.userurl_second, mode='r') as inputfile2:
    for line in inputfile2:
        line = line.rstrip()
        if line == '':
            continue
        user, url = line.split(':', 1)
        users_second.add(user)
        #urls_second.add(url)
        #ドメインベースでの解析
        urls_second.add(urlparse(url).netloc)
        if user not in user_urls_second:
            user_urls_second[user] = {url}
        else:
            user_urls_second[user].add(url)
        # if user not in user_number.values():
        #     user_number[i] = user
        #     i = i + 1
# 共通ユーザ取得

users = users_first & users_second

# 異なる期間で最も類似度が高くなるユーザが自分自身かどうかの判定

sim_method = {'jaccard': jaccard, 'dice': dice,
              'simpson': simpson, 'intersection': count_intersection}

match = 0

for user in users:
    # print(user)
    # 後半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
    max_similarity = -1
    urls = user_urls_first[user]

    # user_first_similarity = {}

    for _user, _urls in user_urls_second.items():
        similarity = sim_method[args.method](urls, _urls)

        with open(re.sub("\\D", "", args.userurl_first) + '_' + re.sub("\\D", "", args.userurl_second)  + args.method + '.txt', 'a') as similarity_record:
            print('second', user.rstrip(), _user.rstrip(), similarity, file=similarity_record)
        # # similarityと_userをplot
        # if similarity != 0:
        #     if _user not in user_first_similarity:
        #         user_first_similarity[_user] = similarity
        #     else:
        #         user_first_similarity[_user].add(similarity)

        if similarity > max_similarity:
            max_similarity = similarity
            max_user = _user
            same_sim_users = {_user}
        elif similarity == max_similarity:
            same_sim_users.add(_user)
    # with open('max_similarity.txt', 'a') as si:
    #     print('first', user, max_user, max_similarity, file=si)

    if len(same_sim_users) == 1:
        if user == max_user:
            match += 1
    elif user in same_sim_users:
        match += 1 / len(same_sim_users)

    # # user_first_similarityのkey名変更
    # i = 1
    # while 1:
    #     if i <= len(user_number):
    #         if user_number[i] in user_first_similarity.keys():
    #             change_dict_key(user_first_similarity, user_number[i], i)
    #         i = i + 1
    #     else:
    #         break

    # 前半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
    max_similarity = -1
    urls = user_urls_second[user]

    # user_second_similarity = {}

    for _user, _urls in user_urls_first.items():
        similarity = sim_method[args.method](urls, _urls)

        with open(re.sub("\\D", "", args.userurl_first) + '_' + re.sub("\\D", "", args.userurl_second) + args.method + '.txt', 'a') as similarity_record:
            print('first', user.rstrip(),  _user.rstrip(), similarity, file=similarity_record)

        # # similarityと_userをplot
        # if similarity != 0:
        #     if _user not in user_second_similarity:
        #         user_second_similarity[_user] = similarity
        #     else:
        #         user_second_similarity[_user].add(similarity)

        if similarity > max_similarity:
            max_similarity = similarity
            max_user = _user
            same_sim_users = {_user}
        elif similarity == max_similarity:
            same_sim_users.add(_user)

    # with open('max_similarity.txt', 'a') as si:
    #     print('second', user, max_user, max_similarity, file=si)

    if len(same_sim_users) == 1:
        if user == max_user:
            match += 1
    elif user in same_sim_users:
        match += 1 / len(same_sim_users)


    # # user_first_similarityのkey名変更
    # i = 1
    # while 1:
    #     if i <= len(user_number):
    #         if user_number[i] in user_second_similarity.keys():
    #             change_dict_key(user_second_similarity, user_number[i], i)
    #         i = i + 1
    #     else:
    #         break

    # # グラフ出力
    # # 画像のプロット先の準備
    # fig = plt.figure()
    # # 散布図の描画
    # for k in range(len(user_number)):
    #     if k in user_first_similarity.keys():
    #         plt.scatter(k, user_first_similarity[k], marker='.', c='aqua')
    #     if k in user_second_similarity.keys():
    #         plt.scatter(k, user_second_similarity[k], marker='.', c='pink')
    #     else:
    #         continue
    # # print(type(user))
    # # keys = [k for k, v in user_number.items() if v == user]
    # # print(type(keys[0]))
    # # グラフの指定
    # keys = [k for k, v in user_number.items() if v == user]
    #
    # plt.title(user +  ' : ' + str(keys[0]))
    # # x方向のラベル
    # plt.xlabel("userid")
    # # y方向のラベル
    # plt.ylabel("similarity")
    # # y方向範囲
    # plt.ylim([0.0,1.0])
    # # グラフをファイルに保存する
    # fig.savefig(user.rstrip() + ".png")
    # plt.close()

# ユーザの一致率を出力
# print('Match rate: {}'.format(match / (2 * len(users))))
with open('result.txt', 'a') as result:
    # print(user_number, file=result)
    print(re.sub("\\D", "", args.userurl_first) + '_' + re.sub("\\D", "", args.userurl_second) , args.method, file=result)
    print('Match rate: {}'.format(match / (2 * len(users))), file=result)
