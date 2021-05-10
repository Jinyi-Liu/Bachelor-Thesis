# -*- coding: utf-8 -*-
import copy
from default_par import *
from model import *
from math import exp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


def comment_on_merchants(perceive_type, mer2buy_id, good_kind, comment_temp, cus):
    # comment_temp[0][mer2buy_id] += (cus.buy_comment_real if perceive_type else cus.buy_comment_fake) * exp(
    #    good_kind / total_good_kinds - 1)
    # comment_temp[0][mer2buy_id] += (
    #    cus.buy_comment_real if perceive_type else (cus.buy_comment_fake * exp(-1 * good_kind / total_good_kinds)))
    prob_comment = random()  # i.e. ie prob_comment <* than the customer will comment on the merchant
    if perceive_type:
        if prob_comment <= cus.prob_comment_on_real[good_kind]:
            comment_temp[0][mer2buy_id] += cus.buy_comment_real
            comment_temp[1][mer2buy_id] += 1
    else:
        comment_temp[0][mer2buy_id] += cus.buy_comment_fake
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


def get_num(par, change_par, select_num):
    temp_num = change_par.get(select_num)
    if temp_num:
        return temp_num
    else:
        return par.get(select_num)


def gen_models(**change_par):
    cus_change_par = change_par['cus']
    mer_change_par = change_par['mer']
    reg_change_par = change_par['reg']
    honest_num = get_num(merchant_par, mer_change_par, 'honest_num')
    speculative_num = get_num(merchant_par, mer_change_par, 'speculative_num')
    cus_num = get_num(customer_par, cus_change_par, 'num')
    reg_num = get_num(regulator_par, reg_change_par, 'num')
    # honest_num = merchant_par['honest_num'] if not mer_change_par.get('honest_num') else mer_change_par['honest_num']
    # speculative_num = merchant_par['speculative_num'] if not mer_change_par.get('speculative_num') else mer_change_par['speculative_num']
    # cus_num = customer_par['num'] if not cus_change_par.get('num') else cus_change_par['num']
    # reg_num = regulator_par['num'] if not reg_change_par.get('num') else reg_change_par['num']

    merchants = [gen_mer_model(ID=i, **mer_change_par) for i in range(speculative_num)] + [
        gen_mer_model(ID=i, fake_rate=[.0 for j in range(general_par['total_good_kinds'])], change_fake_rate=False) for
        i
        in
        range(speculative_num, honest_num + speculative_num)]
    customers = [gen_cus_model(ID=i, **cus_change_par) for i in range(cus_num)]
    regulators = [gen_regulator_model(ID=i, **reg_change_par) for i in range(reg_num)]
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
    mers_fake_rate = [list(mer.fake_rate) for mer in merchants]
    customers_bound = [c.buy_bound for c in customers]
    reg = [reg.fine_got for reg in regulators]
    return [mers_comment, mers_comment_count, mers_money, mers_fake_rate, customers_bound, reg]


def change_fake_rate(mers):
    for mer in mers:
        mer.fake_change()


def game(game_rounds=None, merchants=None, customers=None, regulators=None):
    all_round_data = []
    buy_data = [[None for i in range(len(customers))] for j in range(game_rounds)]
    whether_comment_system = merchants[0].comment_system
    for game_round in range(game_rounds):
        comment_temp = np.zeros((2, len(merchants)))
        for cus_id in range(len(customers)):
            choice_weight = customers[cus_id].buy_good_prob
            good2buy = choices(merchants[0].good_kind, choice_weight)[0]
            perceive_type, mer2buy_id, buy_good_kind, true_type = customers[cus_id].buy(merchants, len(merchants),
                                                                                        good2buy)
            if perceive_type == -1:
                continue  # i.e. no merchant for buying so pass this customer
            if whether_comment_system:
                comment_temp = comment_on_merchants(perceive_type, mer2buy_id, buy_good_kind, comment_temp,
                                                    customers[cus_id])
            buy_data[game_round][cus_id] = [perceive_type, mer2buy_id, buy_good_kind, true_type]
        adjust_one_round_comment(merchants, comment_temp)
        change_fake_rate(merchants)
        temp = get_one_round_data(merchants, customers, regulators)
        all_round_data.append(temp)
        for reg in regulators:
            reg.check_market(mers=merchants)

    return all_round_data, buy_data


def plot_image(data, title,mers):
    speculative_num = mers[0].speculative_num
    honest_num = mers[0].honest_num
    display = [0, speculative_num]
    mers_num = speculative_num+honest_num
    cus_num = len(data[0][4])
    reg_num = len(data[0][5])
    mers_comment = pd.DataFrame([_[0] for _ in data], columns=[i for i in range(mers_num)])
    mers_money = pd.DataFrame([_[2] for _ in data], columns=[i for i in range(mers_num)])
    mers_fake_rate = pd.DataFrame([[a[0] for a in (_[3])] for _ in data], columns=[i for i in range(mers_num)])
    customers_bound_temp = pd.DataFrame([_[4] for _ in data], columns=[i for i in range(cus_num)])
    customers_bound = customers_bound_temp.mean(axis=1)
    reg_fine = pd.DataFrame([_[5] for _ in data], columns=[i for i in range(reg_num)])
    fig, axes = plt.subplots(2, 2, figsize=(10, 10), dpi=300)
    color = ['r' for i in range(speculative_num)] + ['b' for i in range(honest_num)]

    axes[0, 0].plot(mers_comment)
    for i, j in enumerate(axes[0, 0].lines):
        j.set_color(color[i])
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')

    axes[0, 0].set_title("Merchants' Comments")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    axes[0, 0].legend([handle for i, handle in enumerate(handles) if i in display],
                      ['Selling fake', 'Not selling fake'])
    axes[0, 1].set_title("Fine")
    axes[0, 1].plot(reg_fine)

    axes[1, 0].set_title("Merchants' Profit")
    axes[1, 0].legend([handle for i, handle in enumerate(handles) if i in display],
                      ['Selling fake', 'Not selling fake'])
    axes[1, 0].plot(mers_money)
    axes[1, 0].set_xlabel('round')
    for i, j in enumerate(axes[1, 0].lines):
        j.set_color(color[i])

    axes[1, 1].set_title("Customers' Average Bound")
    axes[1, 1].plot(customers_bound)
    axes[1, 1].set_xlabel('round')
    # fig.suptitle(title,fontsize=20)
    plt.show()
    # plt.savefig('./images/'+title)
