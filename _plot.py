import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle


def plot_image(data, title, mers, show):
    speculative_num = mers[0].speculative_num
    honest_num = mers[0].honest_num
    display = [0, speculative_num]
    mers_num = speculative_num + honest_num
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
    if show:
        plt.show()
    else:
        plt.savefig('./images/' + title, bbox_inches='tight')


def plot_monte(title):
    with open('./data/monte_data-' + title + '.pk', 'rb') as f:
        data = pickle.load(f)
    data_set = data[:10]
    buy_data_set = data[10:20]
    mers_average_money = monte(data_set, [5, 5])
    fig, axes = plt.subplots(1, 1, figsize=(5, 5), dpi=300)
    axes.plot(mers_average_money)
    speculative_num, honest_num = [5, 5]
    color = ['r' for i in range(speculative_num)] + ['b' for i in range(honest_num)]
    for i, j in enumerate(axes.lines):
        j.set_color(color[i])
        j.set_label('Selling fake' if i < speculative_num else 'Not Selling fake')
    handles, labels = axes.get_legend_handles_labels()
    display = [0, speculative_num]
    axes.legend([handle for i, handle in enumerate(handles) if i in display],
                ['Selling fake', 'Not selling fake'])
    plt.show()
    # plt.savefig('./image/'+title,bbox_inches='tight')
