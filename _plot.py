import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
from func import *


def plot_image(data, title, mers, show):
    speculative_num = mers[0].speculative_num
    honest_num = mers[0].honest_num
    display = [0, speculative_num]
    mers_num = speculative_num + honest_num
    cus_num = len(data[0][4])
    reg_num = len(data[0][5])
    mers_comment = pd.DataFrame([_[0] for _ in data], columns=[i for i in range(mers_num)])
    mers_money = pd.DataFrame([_[2] for _ in data], columns=[i for i in range(mers_num)])
    # mers_fake_rate = pd.DataFrame([[a[0] for a in (_[3])] for _ in data], columns=[i for i in range(mers_num)])
    customers_bound_temp = pd.DataFrame([_[4] for _ in data], columns=[i for i in range(cus_num)])
    customers_bound = customers_bound_temp.mean(axis=1)
    reg_fine = pd.DataFrame([_[5] for _ in data], columns=[i for i in range(reg_num)])
    reg_cost = pd.DataFrame([_[6] for _ in data], columns=[i for i in range(reg_num)])
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
    axes[0, 1].set_title("Regulators' Fine and Cost")
    axes[0, 1].plot(reg_fine,label='fine',color='b')
    axes[0, 1].plot(reg_cost,label='cost',color='r')
    handles_reg, labels_reg = axes[0, 1].get_legend_handles_labels()
    axes[0, 1].legend([handle for i, handle in enumerate(handles_reg) if i in [0,reg_num]],
                      ['Fine', 'Regulation cost'])

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
    if show:
        plt.show()
    else:
        plt.savefig('./images/' + title, bbox_inches='tight')


def plot_reg_cost(pars_titles, times):
    fig, axes = plt.subplots(2, 1, figsize=(5, 5), dpi=300)
    for i, title in enumerate(pars_titles):
        with open('./data/monte_data-' + title + 'test.pk', 'rb') as f:
            data = pickle.load(f)
        data_set = data[:times]
        reg_num = len(data_set[0][0][6])
        for data in data_set:
            reg_cost = pd.DataFrame([_[6] for _ in data], columns=[i for i in range(reg_num)])
            axes[i].plot(reg_cost)
    plt.show()


def monte_process_plot(data_set):
    speculative_num, honest_num = get_mers_num(data_set)
    mers_total_num = speculative_num + honest_num
    spe_list = []
    hon_list = []
    for data in data_set:
        mers_money = pd.DataFrame([_[2] for _ in data], columns=[i for i in range(mers_total_num)])
        spe = mers_money.iloc[:, :speculative_num]
        hon = mers_money.iloc[:, speculative_num:mers_total_num]
        temp_spe = spe.sort_values(by=999, axis=1).values.T if spe.ndim != 1 else spe.values.T
        temp_hon = hon.sort_values(by=999, axis=1).values.T
        spe_list.append(temp_spe)
        hon_list.append(temp_hon)
    spe_np = np.array(spe_list).mean(axis=0)
    hon_np = np.array(hon_list).mean(axis=0)
    total_ = np.vstack((spe_np, hon_np)).T
    ave_money = pd.DataFrame(total_)
    return ave_money


def plot_monte_average(title, show=True, times=10):
    with open('./data/monte_data-' + title + '.pk', 'rb') as f:
        data = pickle.load(f)
    data_set = data[:times]
    mers_average_money = monte_process_plot(data_set)
    fig, axes = plt.subplots(1, 1, figsize=(5, 5), dpi=300)
    axes.plot(mers_average_money)
    speculative_num, honest_num = get_mers_num(data_set)
    color = ['r' for i in range(speculative_num)] + ['b' for i in range(honest_num)]
    for i, j in enumerate(axes.lines):
        j.set_color(color[i])
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
    handles, labels = axes.get_legend_handles_labels()
    display = [0, speculative_num]
    axes.legend([handle for i, handle in enumerate(handles) if i in display],
                ['Selling fake', 'Not selling fake'])
    if show:
        plt.show()
    else:
        plt.savefig('./images/monte-ave-' + title[-3:], bbox_inches='tight')


def plot_monte_average_all(titles, mers_num, show=True, times=10):
    sub_num = len(titles)
    fig, axes = plt.subplots(1, 1, figsize=(5, 5), dpi=300)
    mers_money_set = []
    for title in titles:
        with open('./data/monte_data-' + title + '.pk', 'rb') as f:
            data = pickle.load(f)
        data_set = data[:times]
        mers_average_money = monte_process_plot(data_set)
        mers_money_set.append(mers_average_money)
    speculative_num, honest_num = get_mers_num(data_set)
    mers_total_num = speculative_num + honest_num
    linestyle_str = ['dashed'] * speculative_num + ['solid'] * honest_num + ['solid'] * mers_total_num
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


def plot_monte_all(title, show=True, times=10):
    with open('./data/monte_data-' + title + '.pk', 'rb') as f:
        data = pickle.load(f)
    data_set = data[:times]
    mers_num = get_mers_num(data_set)
    # buy_data_set = data[times:2 * times]
    mers_money_set = []
    mers_comment_set = []
    for data in data_set:
        mers_money = pd.DataFrame([_[2] for _ in data], columns=[i for i in range(sum(mers_num))])
        mers_money_set.append(mers_money)
        mers_comment = pd.DataFrame([_[0] for _ in data], columns=[i for i in range(sum(mers_num))])
        mers_comment_set.append(mers_comment)

    fig, axes = plt.subplots(2, 1, figsize=(5, 5), dpi=300)

    speculative_num, honest_num = mers_num
    color = ['r' for i in range(speculative_num)] + ['b' for i in range(honest_num)]
    for (mers_money, mers_comment) in zip(mers_money_set, mers_comment_set):
        axes[0].plot(mers_money)
        axes[1].plot(mers_comment)
    for i, j in enumerate(axes[0].lines):
        j.set_color(color[i % sum(mers_num)])
        j.set_alpha(1 - i // sum(mers_num) / times)
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
    for i, j in enumerate(axes[1].lines):
        j.set_color(color[i % sum(mers_num)])
        j.set_alpha(1 - i // sum(mers_num) / times)
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
    handles, labels = axes[0].get_legend_handles_labels()
    display = [0, speculative_num]
    fig.legend([handle for i, handle in enumerate(handles) if i in display],
               ['Selling fake', 'Not selling fake'])
    if show:
        plt.show()
    else:
        plt.savefig('./images/' + 'monte-' + title[-3:], bbox_inches='tight')


def get_mers_num(data_set):
    mer_fake = np.array(data_set[0][0][3])
    good_num = len(mer_fake[0])
    check_temp = [0 for _ in range(good_num)]
    temp = (mer_fake == check_temp)
    temp = [_.all() for _ in temp]
    honest_num = sum(temp)
    speculative_num = len(mer_fake) - honest_num
    return speculative_num, honest_num


def monte_process_ave(data_set, mer_process=True):
    speculative_num, honest_num = get_mers_num(data_set)
    mers_total_num = speculative_num + honest_num
    reg_num = len(data_set[0][0][5])
    spe_list = []
    hon_list = []
    if mer_process:
        for data in data_set:
            temp = pd.DataFrame([_[2] for _ in data], columns=[i for i in range(mers_total_num)])
            spe = temp.iloc[:, :speculative_num]
            hon = temp.iloc[:, speculative_num:mers_total_num]
            temp_spe = spe.sort_values(by=999, axis=1).values.T if spe.ndim != 1 else spe.values.T
            temp_hon = hon.sort_values(by=999, axis=1).values.T
            spe_list.append(temp_spe)
            hon_list.append(temp_hon)
        spe_np = np.array(spe_list).mean(axis=0)
        hon_np = np.array(hon_list).mean(axis=0)
        total_ = np.vstack((spe_np, hon_np)).T
        temp_ = pd.DataFrame(total_)
    else:
        fine_list = []
        for data in data_set:
            temp = pd.DataFrame([_[5] for _ in data], columns=[i for i in range(reg_num)])
            temp_1 = temp.values.T
            fine_list.append(temp_1)
        fine_np = np.array(fine_list).mean(axis=0)
        temp_ = pd.DataFrame(fine_np.T)
    return temp_


def plot_image_4(pars_titles, show):
    mers_money_set = []
    regs_fine_set = []
    for title in pars_titles:
        with open('./data/monte_data-' + title + '.pk', 'rb') as f:
            data = pickle.load(f)
        times = len(data) // 2
        data_set = data[:times]
        mer_money = monte_process_ave(data_set, mer_process=True)
        reg_fine = monte_process_ave(data_set, mer_process=False)
        mers_money_set.append(mer_money)
        regs_fine_set.append(reg_fine)
    speculative_num, honest_num = get_mers_num(data_set)
    mers_total_num = speculative_num + honest_num

    reg_num = len(data_set[0][0][5])
    total_num = mers_total_num + reg_num
    fig, axes = plt.subplots(1, 1, figsize=(7, 5), dpi=300)
    linestyle_str = (['dashed'] * speculative_num + ['solid'] * honest_num + ['dotted'] * reg_num) * len(pars_titles)
    color = ['r'] * total_num + ['g'] * total_num + ['b'] * total_num
    for i, mers_money in enumerate(mers_money_set):
        axes.plot(mers_money)
        axes.plot(regs_fine_set[i])
    for i, j in enumerate(axes.lines):
        j.set_color(color[i])
        j.set_linestyle(linestyle_str[i])
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
        j.set_label('regulator' if mers_total_num < i < total_num else 0)
    handles, labels = axes.get_legend_handles_labels()
    display = np.array([0, speculative_num, mers_total_num,
                        mers_total_num + reg_num,
                        mers_total_num + reg_num + speculative_num,
                        mers_total_num + reg_num + mers_total_num,
                        mers_total_num + reg_num + mers_total_num + reg_num,
                        mers_total_num + reg_num + mers_total_num + reg_num + speculative_num,
                        mers_total_num + reg_num + mers_total_num + reg_num + mers_total_num])
    axes.plot([0], marker='None', linestyle='None', label='4-1')
    axes.plot([0], marker='None', linestyle='None', label='4-2')
    axes.plot([0], marker='None', linestyle='None', label='4-3')
    fig.legend([axes.lines[-3], axes.lines[-2], axes.lines[-1]] * 3 + [handle for i, handle in enumerate(handles) if
                                                                       i in display],
               ['4.4 10x', '', '', '4.5 5x', '', '', '4.6 20x', '', ''] + ['Selling fake', 'Not selling fake',
                                                                           'Regulator'] * 3,
               ncol=2, loc='upper left', )
    if show:
        plt.show()
    else:
        plt.savefig('./images/' + 'model-4_1spe', bbox_inches='tight')


def plot_image_5(pars_titles, show):
    mers_money_set = []
    regs_fine_set = []
    for title in pars_titles:
        with open('./data/monte_data-' + title + '.pk', 'rb') as f:
            data_set = pickle.load(f)
        mer_money = monte_process_ave(data_set, mer_process=True)
        reg_fine = monte_process_ave(data_set, mer_process=False)
        mers_money_set.append(mer_money)
        regs_fine_set.append(reg_fine)
    speculative_num, honest_num = get_mers_num(data_set)
    mers_total_num = speculative_num + honest_num

    reg_num = len(data_set[0][0][5])
    total_num = mers_total_num + reg_num
    fig, axes = plt.subplots(1, 1, figsize=(7, 5), dpi=300)
    linestyle_str = (['dashed'] * speculative_num + ['solid'] * honest_num + ['dotted'] * reg_num) * len(pars_titles)
    color = ['r'] * total_num + ['b'] * total_num
    for i, mers_money in enumerate(mers_money_set):
        axes.plot(mers_money,alpha=1-i/len(mers_money_set))
        axes.plot(regs_fine_set[i])
    for i, j in enumerate(axes.lines):
        j.set_color(color[i])
        j.set_linestyle(linestyle_str[i])
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
        j.set_label('regulator' if mers_total_num < i < total_num else 0)
    handles, labels = axes.get_legend_handles_labels()
    display = np.array([0, speculative_num, mers_total_num,
                        mers_total_num + reg_num,
                        mers_total_num + reg_num + speculative_num,
                        mers_total_num + reg_num + mers_total_num])
    # mers_total_num + reg_num + mers_total_num + reg_num,
    # mers_total_num + reg_num + mers_total_num + reg_num + speculative_num,
    # mers_total_num + reg_num + mers_total_num + reg_num + mers_total_num])
    axes.plot([0], marker='None', linestyle='None', label='5-1')
    axes.plot([0], marker='None', linestyle='None', label='5-2')
    # axes.plot([0], marker='None', linestyle='None', label='4-3')
    fig.legend([axes.lines[-2], axes.lines[-1]] * 3 + [handle for i, handle in enumerate(handles) if
                                                       i in display],
               ['5.3', '', '', '5.4', '', ''] + ['Selling fake', 'Not selling fake', 'Regulator'] * 2,
               ncol=2, loc='upper left')
    if show:
        plt.show()
    else:
        plt.savefig('./images/' + 'model-5_3spe', bbox_inches='tight')
