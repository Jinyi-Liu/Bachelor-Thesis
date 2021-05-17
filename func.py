# -*- coding: utf-8 -*-
import copy
from default_par import *
from model import *
from math import exp
import pandas as pd
import pickle
from random import seed
from _plot import *


def comment_on_merchants(perceive_type, mer2buy_id, good_kind, comment_temp, cus):
    # comment_temp[0][mer2buy_id] += (cus.buy_comment_real if perceive_type else cus.buy_comment_fake) * exp(
    #    good_kind / total_good_kinds - 1)
    # comment_temp[0][mer2buy_id] += (
    #    cus.buy_comment_real if perceive_type else (cus.buy_comment_fake * exp(-1 * good_kind / total_good_kinds)))
    prob_comment = random()  # i.e. ie prob_comment <* than the customer will comment on the merchant
    if perceive_type:
        if prob_comment <= cus.prob_comment_on_real[good_kind]:
            comment_temp[0][mer2buy_id] += cus.buy_comment_real[good_kind]
            comment_temp[1][mer2buy_id] += 1
    else:
        comment_temp[0][mer2buy_id] += cus.buy_comment_fake[good_kind]
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
    good_kind_change = mer_change_par.get('good_kind')

    total_good_kind = general_par['total_good_kinds'] if not good_kind_change else len(good_kind_change)

    temp = {
        'fake_rate': [.0 for j in range(total_good_kind)],
        'change_fake_rate': False,
    }
    speculative_mer_par = copy.deepcopy(mer_change_par)
    speculative_mer_par.update(temp)
    speculative_mers = [gen_mer_model(ID=i, **speculative_mer_par) for i in
                        range(speculative_num, honest_num + speculative_num)]
    merchants = [gen_mer_model(ID=i, **mer_change_par) for i in range(speculative_num)] + speculative_mers

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
    reg_fine = [reg.fine_got for reg in regulators]
    reg_cost = [reg.check_cost for reg in regulators]
    return [mers_comment, mers_comment_count, mers_money, mers_fake_rate, customers_bound, reg_fine,reg_cost]


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
            perceive_type, mer2buy_id, buy_good_kind, true_type = customers[cus_id].buy(merchants, len(merchants))
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


def output_single(pars, pars_titles, show, set_seed):
    for (par, title) in zip(pars, pars_titles):
        seed(set_seed)
        merchants, customers, regulators = gen_models(**par)
        data, buy_data = game(game_rounds=1000, merchants=merchants, customers=customers, regulators=regulators)
        if show:
            plot_image(data, title, mers=merchants, show=show)
        else:
            with open('./data/data-' + title + '.pk', 'wb') as f:
                pickle.dump(data + buy_data, f)
            plot_image(data, title, mers=merchants, show=show)
        mer_profit = data[-1][2]
        mer_comment = data[-1][0]
        print(mer_comment)
        print(np.mean(mer_profit[-5:]) / np.mean(mer_profit[:5]))
        print(np.mean(mer_profit[:5]) / np.mean(mer_profit[-5:]))


def monte_process_data(par, title,times=10):
    data_set = []
    buy_data_set = []
    for i in range(times):
        seed(i)
        merchants, customers, regulators = gen_models(**par)
        data, buy_data = game(game_rounds=1000, merchants=merchants, customers=customers, regulators=regulators)
        data_set.append(data)
        # buy_data_set.append(buy_data)
    with open('./data/monte_data-' + title + '.pk', 'wb') as f:
        pickle.dump(data_set + buy_data_set, f)


def plot_monte_average_4(titles, mers_num, show=True, times=10):
    speculative_num, honest_num = mers_num
    total_num = sum(mers_num)
    sub_num = len(titles)
    fig, axes = plt.subplots(1, 1, figsize=(5, 5), dpi=300)
    mers_money_set = []
    linestyle_str = ['dashed'] * speculative_num + ['solid'] * honest_num + ['solid'] * total_num
    for title in titles:
        with open('./data/monte_data-' + title + '.pk', 'rb') as f:
            data = pickle.load(f)
        data_set = data[:times]
        mers_average_money = monte_process_plot(data_set, mers_num)
        mers_money_set.append(mers_average_money)
    for i, mers_money in enumerate(mers_money_set):
        axes.plot(mers_money)
        color = ['r' for i in range(speculative_num)] + ['b' for i in range(honest_num)] + ['g' for i in
                                                                                            range(sum(mers_num), sum(
                                                                                                mers_num) + speculative_num)] + [
                    'c' for i in range(sum(mers_num) + speculative_num, 2 * sum(mers_num))]
    for i, j in enumerate(axes.lines):
        j.set_color(color[i])
        j.set_linestyle(linestyle_str[i])
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
    handles, labels = axes.get_legend_handles_labels()
    display = [0, speculative_num, sum(mers_num), sum(mers_num) + speculative_num]
    axes.plot([0], marker='None', linestyle='None', label='7-7')
    axes.plot([0], marker='None', linestyle='None', label='7-8')
    fig.legend([axes.lines[-2], axes.lines[-1]] * 2 + [handle for i, handle in enumerate(handles) if i in display],
               ['7.7', '', '7.8', ''] + ['Selling fake', 'Not selling fake'] * 2, ncol=2)
    if show:
        plt.show()
    else:
        plt.savefig('./images/' + 'monte-ave-all-' + title[-3:], bbox_inches='tight')
