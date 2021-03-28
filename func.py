# -*- coding: utf-8 -*-
from model import *
from math import exp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

total_good_kinds = 4  # the number of goods' kind.
fake_margin = 0.2  # fake cost proportionate of price
real_margin = 0.5  # real cost proportionate of price
fake_price_efficiency = 0.9  # TBD! a function of price

# Merchant's default parameter
_comment = [5, 0]  # default comment, comment_count
_good_kind = [x for x in range(total_good_kinds)]  # how many goods one merchant sells
# _fake_rate = [exp(i - total_good_kinds) for i in range(total_good_kinds)]  # TBD
_real_p_par = [10, 100, 500, 5000]  # real_price
_real_c_par = [real_margin * price for price in _real_p_par]  # real_cost
_fake_p_par = [fake_price_efficiency * price for price in _real_p_par]  # fake_price
_fake_c_par = [fake_margin * fake_price for fake_price in _fake_p_par]  # fake_cost
_fake_rate = [0.5, 0.3, 0.1, 0.05]

_bound_par = [3, 0.9, 9, 1.05]  # de_fake_bound & rate, in_fake_bound & rate

# Customer's default parameter
_buy_bound = 5
_identify_fake_rate = [0.05, 0.1, 0.15, 0.3]  # TBD
_buy_good_prob = [0.4,0.3,0.2,0.1]
_buy_bound_par = [0.1, 0.2]  # buy_bound_real & fake
_buy_comment_par = [comment_bound, .5 * comment_bound]  # buy_comment_real & fake
_prob_random = 0.2  # the probability that one buys something randomly

# Regulator's default parameter
_lazy_par = [0.8, 0.01]  # lazy_fake_rate; lazy_cost_rate
_diligent_par = [1, 0.2]  # diligent_fake_rate, diligent_cost_rate
_punishment_par = [10, 0.2]  # punishment_money, punishment_comment


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
    #comment_temp[0][mer2buy_id] += (cus.buy_comment_real if perceive_type else cus.buy_comment_fake) * exp(
    #    good_kind / total_good_kinds - 1)
    comment_temp[0][mer2buy_id] += (cus.buy_comment_real if perceive_type else (cus.buy_comment_fake * exp(-1*good_kind/total_good_kinds) ))
    comment_temp[1][mer2buy_id] += 1
    return comment_temp


def gen_mer_model(mer_id=None, comment=None, good_kind=None, fake_rate=_fake_rate, fake_c_par=_fake_c_par,
                  fake_p_par=None, real_c_par=_real_c_par, real_p_par=_real_p_par, bound_par=_bound_par):
    if good_kind is None:
        good_kind = _good_kind
    if comment is None:
        comment = _comment
    if fake_p_par is None:
        fake_p_par = _fake_p_par
    par = [mer_id, comment, good_kind, fake_rate, [fake_c_par, fake_p_par], [real_c_par, real_p_par], bound_par]
    mer = Merchant(par)
    return mer


def gen_cus_model(cus_id=None, buy_bound=_buy_bound, buy_good_prob=_buy_good_prob,identify_fake_rate=_identify_fake_rate,
                  buy_bound_par=_buy_bound_par,
                  buy_comment_par=_buy_comment_par, prob_random=_prob_random):
    par = [cus_id, buy_bound,buy_good_prob, identify_fake_rate, buy_bound_par, buy_comment_par, prob_random]
    cus = Customer(par)
    return cus


def gen_regulator_model(reg_id=None, lazy_par=_lazy_par, diligent_par=_diligent_par, punishment_par=_punishment_par):
    par = [reg_id, lazy_par, diligent_par, punishment_par]
    regulator = Regulator(par)
    return regulator


def gen_models(mer_num=5, cus_num=100, regulators_num=5):
    merchants = [gen_mer_model(i) for i in range(mer_num)]+[gen_mer_model(i, fake_rate=[.0 for j in range(total_good_kinds)]) for i in range(mer_num,2*mer_num)]
    # merchants = [gen_mer_model(i,fake_rate=[.0,.0,.0,.0]) for i in range(mer_num)]
    customers = [gen_cus_model(i) for i in range(cus_num)]
    regulators = [gen_regulator_model(i) for i in range(regulators_num)]
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
    reg = regulators[0].fine_got
    return [mers_comment, mers_comment_count, mers_money, mers_fake_rate, customers_bound, reg]


def change_fake_rate(mers):
    for mer in mers:
        mer.fake_change()


def game(game_rounds=500):
    mers, customers, regs = gen_models()
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
        regs[0].check_market(lazy=False, mers=mers)

    return all_round_data, buy_data


def plot_image(data):
    mers_num = len(data[0][0])
    mers_comment = pd.DataFrame([_[0] for _ in data],columns=[i for i in range(mers_num)])
    mers_money = pd.DataFrame([_[2] for _ in data],columns=[i for i in range(mers_num)])
    mers_fake_rate = pd.DataFrame([_[3] for _ in data],columns=[i for i in range(mers_num)])
    customers_bound = pd.DataFrame([_[4] for _ in data],columns=[i for i in range(mers_num)])
    reg_find = pd.DataFrame([_[5] for _ in data],columns=[i for i in range(mers_num)])
    fig, axes = plt.subplots(2, 2,figsize=(10,10))
    # plt.subplots_adjust(wspace=0.2, hspace=0.5)
    mers_comment.plot(ax=axes[0,0],)
    axes[0,0].set_title("Merchants' Comments")
    mers_money.plot(ax=axes[0,1])
    axes[0,1].set_title("Merchants' Profit")
    mers_fake_rate.plot(ax=axes[1,0])
    axes[1,0].set_title("Merchants' fake rate")
    plt.show()

