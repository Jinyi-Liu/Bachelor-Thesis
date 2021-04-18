# -*- coding: utf-8 -*-
import copy
from default_par import *
from model import *
from math import exp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


def comment_on_merchants(perceive_type, mer2buy_id, good_kind, comment_temp, cus):
    """
    May be need some changes on the comment method? E.g. if the good price is high then the comment will be more strong?
    :param perceive_type:
    :param mer2buy_id:
    :param good_kind:
    :param comment_temp:
    :param comment_count:
    :param cus:
    :return:
    """
    # comment_temp[0][mer2buy_id] += (cus.buy_comment_real if perceive_type else cus.buy_comment_fake) * exp(
    #    good_kind / total_good_kinds - 1)
    # comment_temp[0][mer2buy_id] += (
    #    cus.buy_comment_real if perceive_type else (cus.buy_comment_fake * exp(-1 * good_kind / total_good_kinds)))
    comment_temp[0][mer2buy_id] += cus.buy_comment_change_real if perceive_type else cus.buy_comment_change_fake
    comment_temp[1][mer2buy_id] += 1
    return comment_temp


def gen_mer_model(**mer_change_par):
    default_par = copy.deepcopy(merchant_par)
    for par_tbc, value in mer_change_par.items():
        default_par[par_tbc] = value
    merchant = Merchant(**default_par)
    return merchant


def gen_cus_model(**cus_change_par):
    default_par = copy.deepcopy(customer_par)
    for par_tbc, value in cus_change_par.items():
        default_par[par_tbc] = value
    customer = Customer(**default_par)
    return customer


def gen_regulator_model(**reg_change_par):
    default_par = copy.deepcopy(regulator_par)
    for par_tbc, value in reg_change_par.items():
        default_par[par_tbc] = value
    regulator = Regulator(**default_par)
    return regulator


def gen_models(mer_num=5, cus_num=100, regulators_num=5, **change_par):
    cus_change_par = change_par['cus']
    mer_change_par = change_par['mer']
    reg_change_par = change_par['reg']
    merchants = [gen_mer_model(ID=i, **mer_change_par) for i in range(mer_num)]
    #            + [
    #    gen_mer_model(ID=i, fake_rate=[.0 for j in range(global_par['total_good_kinds'])]) for i in
    #    range(mer_num, 2 * mer_num)]
    # merchants = [gen_mer_model(i,fake_rate=[.0,.0,.0,.0]) for i in range(mer_num)]
    customers = [gen_cus_model(ID=i, **cus_change_par) for i in range(cus_num)]
    regulators = [gen_regulator_model(ID=i, **reg_change_par) for i in range(regulators_num)]
    return merchants, customers, regulators


def adjust_one_round_comment(mers, comment_temp):
    for mer in mers:
        comment = comment_temp[0][mer.ID]
        comment_num = comment_temp[1][mer.ID]
        if comment:
            mer.comment = ((mer.comment * mer.comment_count) + comment) / (mer.comment_count + comment_num)
            mer.comment_count += comment_num
        mer.adjust_comment()


def get_one_round_data(merchants, customers, regulators):
    mers_comment = [mer.comment for mer in merchants]
    mers_comment_count = [mer.comment_count for mer in merchants]
    mers_money = [mer.money for mer in merchants]
    mers_fake_rate = [list(mer.fake_rate) for mer in merchants]  # interesting!
    customers_bound = [c.buy_bound for c in customers]
    reg = [reg.fine_got for reg in regulators]
    return [mers_comment, mers_comment_count, mers_money, mers_fake_rate, customers_bound, reg]


def change_fake_rate(mers):
    for mer in mers:
        mer.fake_change()


def game(game_rounds=6000,**change_par):
    mers, customers, regs = gen_models(**change_par)
    all_round_data = []
    buy_data = [[None for i in range(len(customers))] for j in range(game_rounds)]
    for game_round in range(game_rounds):
        comment_temp = np.zeros((2, len(mers)))
        for cus_id in range(len(customers)):
            choice_weight = customers[cus_id].buy_good_prob
            good2buy = choices(mers[0].good_kind, choice_weight)[0]
            perceive_type, mer2buy_id, good_kind, true_type = customers[cus_id].buy(mers, len(mers), good2buy)
            if perceive_type == -1:
                continue  # i.e. no merchant for buying so pass this customer
            comment_temp = comment_on_merchants(perceive_type, mer2buy_id, good_kind, comment_temp, customers[cus_id])
            buy_data[game_round][cus_id] = [perceive_type, mer2buy_id, good_kind, true_type]
        adjust_one_round_comment(mers, comment_temp)
        change_fake_rate(mers)
        temp = get_one_round_data(mers, customers, regs)
        all_round_data.append(temp)
        for reg in regs:
            reg.check_market(lazy=False, mers=mers)

    return all_round_data, buy_data


def plot_image(data):
    mers_num = len(data[0][0])
    cus_num = 100
    reg_num = 5
    mers_comment = pd.DataFrame([_[0] for _ in data], columns=[i for i in range(mers_num)])
    mers_money = pd.DataFrame([_[2] for _ in data], columns=[i for i in range(mers_num)])
    mers_fake_rate = pd.DataFrame([_[3] for _ in data], columns=[i for i in range(mers_num)])
    customers_bound = pd.DataFrame([_[4] for _ in data], columns=[i for i in range(cus_num)])
    reg_find = pd.DataFrame([_[5] for _ in data], columns=[i for i in range(reg_num)])
    fig, axes = plt.subplots(2, 2, figsize=(10, 10), dpi=300)
    color = [cm.autumn(i) for i in range(1, 20, 4)] + [cm.winter(i) for i in range(1, 20, 4)]
    # plt.subplots_adjust(wspace=0.2, hspace=0.5)
    mers_comment.plot(ax=axes[0, 0], color=color)
    axes[0, 0].set_title("Merchants' Comments")
    reg_find.plot(ax=axes[0, 1])
    axes[0, 1].set_title("Fine")
    mers_money.plot(ax=axes[1, 0], color=color)
    axes[1, 0].set_title("Merchants' Profit")
    customers_bound.mean().plot(ax=axes[1, 1], legend=False)
    axes[1, 1].set_title("Customers' Bound")
    plt.show()
