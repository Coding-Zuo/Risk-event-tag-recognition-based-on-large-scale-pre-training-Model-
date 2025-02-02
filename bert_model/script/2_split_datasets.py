# -*- coding:utf-8 -*-
import os
import random
from collections import defaultdict


def split_train(train_file, dev_ratio=0.2, to_folder=None):
    with open(train_file, 'r', encoding='utf-8') as f:
        dict_label_name2sents = defaultdict(list)
        for i, line in enumerate(f):
            if i == 0: continue

            line = line.strip()
            if not line: continue

            id, sent, label_name = line.split(",")
            dict_label_name2sents[label_name].append(sent)

        to_train_file = os.path.join(to_folder, 'train.txt')
        to_dev_file = os.path.join(to_folder, 'dev.txt')

        train_samples = []
        dev_samples = []

        for label_name, sents in dict_label_name2sents.items():
            random.shuffle(sents)

            train_sents_ = sents[int(dev_ratio * len(sents)) + 1:]
            dev_sents_ = sents[:int(dev_ratio * len(sents)) + 1:]

            train_samples.extend([(w, label_name) for w in train_sents_])
            dev_samples.extend([(w, label_name) for w in dev_sents_])

        for samps, file_path in zip([train_samples, dev_samples], [to_train_file, to_dev_file]):
            f_out = open(file_path, 'w', encoding='utf-8')
            for i, samp in enumerate(samps):
                f_out.write("%d,%s,%s" % (i, samp[0], samp[1]) + "\n")


def dev_add_id(dev_file, orgi_train, dev_output_file):
    with open(orgi_train, 'r', encoding='utf-8') as f:
        train_data = dict()
        for i, line in enumerate(f):
            if i == 0: continue

            line = line.strip()
            if not line: continue

            id_, sent, label_name = line.split(",")
            train_data[sent] = id_

    f_out = open(dev_output_file, 'w', encoding='utf-8')
    with open(dev_file, 'r', encoding='utf-8') as f:
        dev_data = []
        for i, line in enumerate(f):
            line = line.strip()
            if not line: continue
            idx, sent, label_name, _ = line.split(",")
            id_ = train_data[sent]
            f_out.write("%d,%s,%s,%d" % (int(idx), sent, label_name, int(id_)) + "\n")


def split_train_quchong(num, train_file, dev_ratio=0.2, to_folder=None):
    with open(train_file, 'r', encoding='utf-8') as f:
        dict_label_name2sents = defaultdict(list)
        for i, line in enumerate(f):
            if i == 0: continue

            line = line.strip()
            if not line: continue

            id, sent, label_name = line.split(",")
            dict_label_name2sents[label_name].append(id + "_" + sent)

        to_train_file = os.path.join(to_folder, 'train.txt')
        to_dev_file = os.path.join(to_folder, 'dev.txt')

        train_samples = []
        dev_samples = []
        print(num)
        for label_name, sents in dict_label_name2sents.items():
            # random.shuffle(sents)
            step = int(dev_ratio * len(sents)) + 1
            r1 = step * num
            r2 = step * (num + 1)
            if num == 0:
                dev_sents_ = sents[r1:r2]
                mid = sents[r2]
                mid_1 = sents[r2 - 1]
                train_sents_ = sents[r2:]
            elif num == 1 or num == 2:
                dev_sents_ = sents[r1:r2]
                mid = sents[r2]
                rr1 = sents[r1]
                train_sents_ = sents[r2:] + sents[0:r1]
            else:
                mid = sents[r1]
                train_sents_ = sents[:r1]
                dev_sents_ = sents[r1:r2]

            train_samples.extend([(w, label_name) for w in train_sents_])
            dev_samples.extend([(w, label_name) for w in dev_sents_])

        num_fold = 0
        for samps, file_path in zip([train_samples, dev_samples], [to_train_file, to_dev_file]):
            f_out = open(file_path, 'w', encoding='utf-8')
            for i, samp in enumerate(samps):
                id_ = samp[0].split("_")[0]
                sent = samp[0].split("_")[1]
                num_fold += 1
                f_out.write("%d,%s,%s,%d" % (i, sent, samp[1], int(id_)) + "\n")
        print("第", num, ":", num_fold)


def split_train_quchong6(num, train_file, dev_ratio=0.2, to_folder=None):
    with open(train_file, 'r', encoding='utf-8') as f:
        dict_label_name2sents = defaultdict(list)
        for i, line in enumerate(f):
            if i == 0: continue

            line = line.strip()
            if not line: continue

            id, sent, label_name = line.split(",")
            dict_label_name2sents[label_name].append(id + "_" + sent)

        to_train_file = os.path.join(to_folder, 'train.txt')
        to_dev_file = os.path.join(to_folder, 'dev.txt')

        train_samples = []
        dev_samples = []
        print(num)
        for label_name, sents in dict_label_name2sents.items():
            # random.shuffle(sents)
            step = int(dev_ratio * len(sents)) + 1
            r1 = step * num
            r2 = step * (num + 1)
            if num == 0:
                dev_sents_ = sents[r1:r2]
                mid = sents[r2]
                mid_1 = sents[r2 - 1]
                train_sents_ = sents[r2:]
            elif num == 1 or num == 2 or num == 3:
                dev_sents_ = sents[r1:r2]
                mid = sents[r2]
                rr1 = sents[r1]
                train_sents_ = sents[r2:] + sents[0:r1]
            elif num == 4:
                dev_sents_ = sents[r1:r2]
                # mid = sents[r2]
                # rr1 = sents[r1]
                train_sents_ = sents[r2:] + sents[0:r1]
            else:
                # mid = sents[r1]
                lens = len(sents)
                r = lens - r2
                if r > 0:
                    train_sents_ = sents[:r1]
                    dev_sents_ = sents[r1:r2]
                else:
                    dev_sents_ = sents[r1:lens] + sents[0:-r]
                    train_sents_ = sents[-r:r1]

            train_samples.extend([(w, label_name) for w in train_sents_])
            dev_samples.extend([(w, label_name) for w in dev_sents_])

        num_fold = 0
        for samps, file_path in zip([train_samples, dev_samples], [to_train_file, to_dev_file]):
            f_out = open(file_path, 'w', encoding='utf-8')
            for i, samp in enumerate(samps):
                id_ = samp[0].split("_")[0]
                sent = samp[0].split("_")[1]
                num_fold += 1
                f_out.write("%d,%s,%s,%d" % (i, sent, samp[1], int(id_)) + "\n")
        print("第", num, ":", num_fold)


def split_train_to_5folds(train_file, to_folder, num_folds=5):
    os.makedirs(to_folder, exist_ok=True)

    for i in range(num_folds):
        to_folder_i = os.path.join(to_folder, "fold_%d" % i)
        os.makedirs(to_folder_i, exist_ok=True)
        # split_train_quchong6(i, train_file, dev_ratio=0.167, to_folder=to_folder_i)
        split_train_quchong(i, train_file, dev_ratio=0.25, to_folder=to_folder_i)


if __name__ == '__main__':
    train_file = "/data2/code/DaguanFengxian/bert_model/data/datagrand_2021_train.csv"
    to_folder = "/data2/code/DaguanFengxian/bert_model/data/splits_quchong6/"
    split_train_to_5folds(train_file, to_folder, num_folds=6)

    dev_file = "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert120k_0/dev.txt"
    dev_output_file = "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert120k_0/dev_qu.txt"

    dev_file_list = [
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_0/dev.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_1/dev.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_2/dev.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_3/dev.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_4/dev.txt",
    ]

    dev_out_file_list = [
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_0/dev_.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_1/dev_.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_2/dev_.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_3/dev_.txt",
        "/data2/code/DaguanFengxian/bert_model/data/splits_quchong1/fold_4/dev_.txt",
    ]
    # dev_file_list = [
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_0/dev.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_1/dev.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_2/dev.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_3/dev.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_4/dev.txt",
    # ]
    #
    # dev_out_file_list = [
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_0/dev_.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_1/dev_.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_2/dev_.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_3/dev_.txt",
    #     "/data2/code/DaguanFengxian/bert_model/data/splits/fold_bert300_4/dev_.txt",
    # ]

    # for d1, d2 in zip(dev_file_list, dev_out_file_list):
    #     dev_add_id(d1, train_file, d2)

    print("finish")
