# -*- coding:utf-8 -*-
"""
    IMPORTING LIBS
"""
import numpy as np
import pandas as pd
import os
import logging
import socket
import time
import random
import glob
import argparse, json
import pickle

import torch
import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim
from torch.utils.data import DataLoader
from os.path import join
from tensorboardX import SummaryWriter

from tqdm import tqdm
from tqdm import trange
from transformers import get_linear_schedule_with_warmup, get_cosine_schedule_with_warmup
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, WeightedRandomSampler
import torchsnooper
from collections import Counter

"""
    IMPORTING CUSTOM MODULES/METHODS
"""
import sys
sys.path.append("/data2/code/DaguanFengxian/bert_model")

from models.model_envs import MODEL_CLASSES
from dataload.data_loader_bert import load_and_cache_examples
from training.Trainer import Trainer
from dataload.data_loader_bert import get_labels

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["CUDA_VISIBLE_DEVICES"] = '1'
model_root_path = "/data2/code/DaguanFengxian/bert_model/data/outputs/"

checkpoint_list_six = [
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    # "new_ensemble/train.bert120k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold4__v3",  # 0.5608
    "4zhe/train.newnezha_dice_supcon_lr1e-5_nomulti_fgm__fold2__v3",
    "final_ensemble/train.bert300_dice_supcon_nolstmgru_lr2e-5_pgd__fold0__v3",  # 0.5669
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
]

checkpoint_list_seven = [  # 0.5822
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "new_ensemble/train.bert120k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold4__v3",  # 0.5608
    "4zhe/train.newnezha_dice_supcon_lr1e-5_nomulti_fgm__fold2__v3",
    "4zhe/train.newnezha_dice_supcon_lr1e-5_nomulti_fgm__fold1__v3",
    "4zhe/train.newnezha_dice_supcon_lr1e-5_nomulti_fgm__fold0__v3",
    "4zhe/train.newnezha_dice_supcon_lr1e-5_nomulti_fgm__fold3__v3",
    "final_ensemble/train.bert300_dice_supcon_nolstmgru_lr2e-5_pgd__fold0__v3",  # 0.5669
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold0__v3",
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold3__v3",
]

checkpoint_list_eight = [
    "final_ensemble/train.bert300_dice_supcon_nolstmgru_lr2e-5_pgd__fold0__v3",  # 0.5669
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
]

checkpoint_list_nine = [
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "final_ensemble/train.bert300_dice_supcon_nolstmgru_lr2e-5_pgd__fold0__v3",  # 0.5669
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
]

checkpoint_list_ten = [
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "final_ensemble/train.bert300_dice_supcon_nolstmgru_lr2e-5_pgd__fold0__v3",  # 0.5669
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
]

checkpoint_list_11 = [
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
]

checkpoint_list_12 = [
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "new_ensemble/train.bert120k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold4__v3",  # 0.5608
    "4zhe/train.newnezha_dice_supcon_lr1e-5_nomulti_fgm__fold2__v3",
    "final_ensemble/train.bert300_dice_supcon_nolstmgru_lr2e-5_pgd__fold0__v3",  # 0.5669
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
    "4zhe/train.nezha110000_dice_supcon_lr1e-5_pgd__fold3__v38",  # 0.570 xia
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1_plabel__v3",  # 0.583 xia
    "4zhe/train.newbert300_dice_supcon_lr1e-5_57__fold2__v3",  # 0.56 xia
    "4zhe/train.nezha120000_dice_supcon_lr1e-5_pgd__fold0__v3",  # 0.56 xia
]

checkpoint_list_13 = [
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1_plabel__v3",  # 0.583 xia
]

checkpoint_list_14 = [
    # 0.5697
    "new_ensemble/train.bert150k_ce_supcon_0.1_0.5_sace_dr_msdrop_sum_4_0.4_multi_hongfan_grulstm_fold0_fgm__v3",
    "final_ensemble/train.newnezha_dice_supcon_lr7e-5_fgm_drpooler__fold0__v3",  # 0.5682
    "4zhe/train.newbert300_dice_supcon_lr1e-5_pgd__fold1__v3",  # 0.5857
]

checkpoint_list = checkpoint_list_14


def full_args(args):
    if not hasattr(args, 'use_ms_dropout'):
        args.use_ms_dropout = False
    if not hasattr(args, 'use_hongfan'):
        args.use_hongfan = False
    if not hasattr(args, 'contrastive_loss'):
        args.contrastive_loss = None
    if not hasattr(args, 'use_focal_loss'):
        args.use_focal_loss = False
    if not hasattr(args, 'use_freelb'):
        args.use_freelb = False
    if not hasattr(args, 'use_multi_task'):
        args.use_multi_task = False
    if not hasattr(args, 'use_gru'):
        args.use_gru = False
    if not hasattr(args, 'use_swa'):
        args.use_swa = False


results_label_list = []
results_logits_list = []
preds_level_2_prob_list = []
avg_weight = []

"""
    读入队友
"""
duiyou_data_dir = "/data2/code/DaguanFengxian/bert_model/data/ensemble_data/0917/"
# bert300_570_prob = pd.read_csv(duiyou_data_dir + "bert300_570.csv").values
newBert_589_prob = pd.read_csv(duiyou_data_dir + "newBert_589.csv").values
nezha300_577_prob = pd.read_csv(duiyou_data_dir + "nezha300_577.csv").values
nezha11w_582_prob = pd.read_csv(duiyou_data_dir + "nezha11w_582.csv").values  # nine
pesudoLabel_582_prob = pd.read_csv(duiyou_data_dir + "pesudoLabel_582.csv").values
nezha8w_570_prob = pd.read_csv(duiyou_data_dir + "nezha8w_570.csv").values  # ten
nezha300_pLabel_575 = pd.read_csv(duiyou_data_dir + "nezha300_pLabel_575.csv").values  # ten

# preds_level_2_prob_list.append(bert300_570_prob.tolist())
preds_level_2_prob_list.append(newBert_589_prob.tolist())
preds_level_2_prob_list.append(nezha300_577_prob.tolist())
preds_level_2_prob_list.append(nezha11w_582_prob.tolist())
preds_level_2_prob_list.append(pesudoLabel_582_prob.tolist())
# preds_level_2_prob_list.append(nezha8w_570_prob.tolist())
preds_level_2_prob_list.append(nezha300_pLabel_575.tolist())
duiyou_len = len(preds_level_2_prob_list)

for preds_level_2 in preds_level_2_prob_list:
    max_logits = np.max(preds_level_2, axis=1).tolist()
    preds_level_2_max = np.argmax(preds_level_2, axis=1)
    list_preds_level_2 = preds_level_2_max.tolist()
    results_label_list.append(list_preds_level_2)

for i, checkpoint_path in enumerate(checkpoint_list):
    logger.info("********** start:" + checkpoint_path + "**********")
    checkpoint_path = model_root_path + checkpoint_path
    args = torch.load(os.path.join(checkpoint_path + '/training_args_bin'))
    full_args(args)

    if "bert120k" in checkpoint_path:
        avg_weight.append(1)
    elif "nezha_base_wwm" in checkpoint_path:
        avg_weight.append(0.8)
    elif "bert_base" in checkpoint_path:
        avg_weight.append(0.7)
    elif "albert" in checkpoint_path:
        avg_weight.append(0.6)

    tokenizer = MODEL_CLASSES[args.model_encoder_type][2].from_pretrained(args.encoder_name_or_path)
    test_dataset, test_sample_weights = load_and_cache_examples(args, tokenizer, mode="test")

    trainer = Trainer(
        args,
        test_dataset=test_dataset,
        test_sample_weights=test_sample_weights,
    )

    trainer.load_model()
    list_preds_level_2, logits_level_2, preds_level_2_prob, _, _ = trainer.ensemble_test("test")  # [6004,35]

    results_label_list += [list_preds_level_2]  # [check_i,idx_sample]
    results_logits_list.append(logits_level_2)  # [check_i,idx_sample]
    preds_level_2_prob_list.append(preds_level_2_prob)  # [check_i,idx_sample,35]
    logger.info("********** end:" + checkpoint_path + "**********")

true_labels = get_labels("/data2/code/DaguanFengxian/bert_model/data/labels_level_2.txt")
"""
    vote
"""


def prob_avg_rank_in_list(prob, prob_list_np):  # 求一个数在二维数组每行的排名，然后求均值
    rank_list = []

    for i, element in enumerate(prob_list_np):
        rank = 0
        for p in element:
            if prob[i] < p:  # 概率大的放前面
                rank += 1
        rank_list.append(rank)

    return np.array(rank_list).mean()


vote_flag = 2  # 0 相同取靠前 1 相同取概率最大 2 相同取平均排名最高的
###### 是否使用相同投票 使用概率加和
vote_label_idx = []
len_test = len(results_label_list[0])
same_num = 0
num_most_2 = 0
num_most_3_ = 0
num_change = 0
for i in range(len_test):
    pred_list_i = []
    prob_list_i = []  # 每个模型 预测本条test的概率 [model_num, 35]
    for j in range(len(checkpoint_list) + duiyou_len):
        pred_list_i.append(results_label_list[j][i])
        prob_list_i.append(preds_level_2_prob_list[j][i])

    if vote_flag == 1:
        ####### 票数相同选概率和最大的
        most_ = Counter(pred_list_i).most_common(35)
        max_vote_num = most_[0][1]
        most_ = [m for m in most_ if m[1] != 1]  # 剔除1票的相同者
        most_ = [m for m in most_ if m[1] == max_vote_num]  # 只选择等于投票最大值的
        if len(most_) == 0:  # 如果全是1票
            vote_label_idx.append(Counter(pred_list_i).most_common(1)[0][0])
        elif len(most_) == 1:
            vote_label_idx.append(most_[0][0])
        else:
            prob_list_np = np.array(prob_list_i)
            select_prob = -1
            select_m = -1
            same_num += 1
            for m, num in most_:
                # 拿概率第m列（所有模型对第m列的概率）求和
                prob_m = prob_list_np[:, m].sum()
                if select_prob < prob_m:
                    select_prob = prob_m
                    select_m = m
            vote_label_idx.append(select_m)
    elif vote_flag == 2:
        ####### 票数相同选平均rank最大的
        most_ = Counter(pred_list_i).most_common(35)
        if len(most_) > 1:
            num_most_2 += 1
            # if len(most_) == 2 and random.uniform(0, 1) >= 0.9:  # 随机反转投票结果
            #     rand = random.randint(0, len(most_) - 1)
            #     vote_label_idx.append(most_[rand][0])
            #     continue
        if len(most_) > 2:
            num_most_3_ += 1
            # if len(most_) > 3 and random.uniform(0, 1) >= 0.92:  # 随机反转投票结果
            #     rand = random.randint(0, len(most_) - 1)
            #     flag = 0  # 票数相同
            #     for m in most_:
            #         if m[1] != most_[0][1]:  # 如果不一样
            #             flag = 1  # 票数不同
            #             break
            #     if flag == 1:
            #         if rand != 0: num_change += 1
            #         vote_label_idx.append(most_[rand][0])
            #         continue
        max_vote_num = most_[0][1]
        most_ = [m for m in most_ if m[1] != 1]  # 剔除1票的相同者
        most_ = [m for m in most_ if m[1] == max_vote_num]  # 只选择等于投票最大值的
        if len(most_) == 0:  # 如果全是1票
            vote_label_idx.append(Counter(pred_list_i).most_common(1)[0][0])
        elif len(most_) == 1:
            vote_label_idx.append(most_[0][0])
        else:
            prob_list_np = np.array(prob_list_i)
            select_rank = -1
            select_m = -1
            same_num += 1
            for m, num in most_:
                # 拿概率第m列（所有模型对第m列的概率）求和
                prob_m = prob_list_np[:, m]
                prob_m_avgrank = prob_avg_rank_in_list(prob_m, prob_list_np)
                if select_rank > prob_m_avgrank:  # 选择排名小的 靠前的
                    select_rank = prob_m_avgrank
                    select_m = m
            vote_label_idx.append(select_m)
    else:
        vote_label_idx.append(Counter(pred_list_i).most_common(1)[0][0])  # 相同的取vote_label_idx.append(most_[rand][0])第一个

print("相同的投票样本有多少：", same_num)
print("有两个及以上结果的：", num_most_2)
print("有三个及以上结果的", num_most_3_)
print("翻转个数", num_change)

"""
    save
"""

f_out = open(os.path.join("/data2/code/DaguanFengxian/bert_model/data/ensemble_data/0917/09.21_14.csv"),
             "w", encoding="utf-8")
f_out.write("id,label" + "\n")
for i, pred_label_id in enumerate(vote_label_idx):
    pred_label_name_level_2 = true_labels[pred_label_id]
    f_out.write("%s,%s" % (str(i), str(pred_label_name_level_2)) + "\n")
