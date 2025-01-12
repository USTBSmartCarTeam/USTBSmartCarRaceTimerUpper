#!/usr/bin/env python3
# 北京科技大学智能汽车竞赛第二次分站赛抽签代码

import random


def generate_order(group, seed):
    group_dict = {
        "摄像头组": 18,
        "电磁组": 16
    }

    if group not in group_dict:
        raise ValueError(f"未知的组别: {group}")

    # 修改为从1开始编号
    order = [f"{'A' if group == '摄像头组' else 'B'}{i}" for i in range(1, group_dict[group] + 1)]

    random.seed(seed)
    random.shuffle(order)
    return order


seed = 11212531320410  # 设置随机种子(本周六超级大乐透开奖号码,开奖后自行设置)
group = "摄像头组"
shuffled_order = generate_order(group, seed)
print(shuffled_order)
