import numpy as np
import copy


def update_par(default_par, par):
    for key in default_par.keys():
        default_par[key].update(par[key])
    return default_par


# Global parameters
general_par = {
    'fake_margin': 0.2,
    "real_margin": 0.5,
    "fake_price_coefficient": 1,
    "real_price": [10],
    'prob_buy_good': [1],
    'identify_fake_rate': np.array([0.05]),
    'fake_rate': np.array([0.3]),
    'comment_system': True,
}
general_par["total_good_kinds"] = len(general_par["real_price"])
general_par["real_cost"] = [general_par['real_margin'] * price for price in general_par['real_price']]
general_par["fake_price"] = list(np.array(general_par["fake_price_coefficient"]) * np.array(general_par["real_price"]))
general_par["fake_cost"] = list(np.array(general_par['fake_price'] * np.array(general_par['fake_margin'])))
# Merchant's default parameter
good_kind = [x for x in range(general_par['total_good_kinds'])]
real_p_par = general_par['real_price']
real_c_par = general_par['real_cost']
fake_p_par = [general_par['fake_price_coefficient'] * price for price in real_p_par]  # fake_price
fake_c_par = [general_par['fake_margin'] * fake_price for fake_price in fake_p_par]  # fake_cost

merchant_par = {
    'speculative_num': 5,
    'honest_num': 5,
    'comment': 5,
    'comment_bound': 10,
    'comment_count': 0,
    'good_kind': good_kind,
    'fake_rate': general_par['fake_rate'],
    'fake_rate_lower_bound': 0,
    'fake_rate_upper_bound': 0.5,
    'fake_price': fake_p_par,
    'fake_cost': fake_c_par,
    'real_price': real_p_par,
    'real_cost': real_c_par,
    'decrease_fake_bound': 3,
    'decrease_fake_rate': np.array([0.05]),
    'increase_fake_bound': 8,
    'increase_fake_rate': np.array([0.02]),
    'change_fake_rate': False,
    'comment_system': general_par['comment_system'],
    # 'fake_sell':[True],
}

# Customer's default parameter
customer_par = {
    'num': 100,
    'buy_bound': 5,
    'prob_buy_good': general_par['prob_buy_good'],
    'identify_fake_rate': general_par['identify_fake_rate'],
    'buy_bound_change_real': [0.2],
    'buy_bound_change_fake': [0.5],
    'buy_comment_real': [1 * merchant_par['comment_bound']],
    'buy_comment_fake': [.5 * merchant_par['comment_bound']],
    'prob_random_buy': 0.0,
    'prob_comment_on_real': [1.0],
    'buy_with_weights': False,
    'learning_fake_rate': 0,
}

# Regulator's default parameter
regulator_par = {
    'num': 5,
    'lazy_identify_rate': .8,
    'lazy_cost_rate': .2,
    'diligent_identify_rate': 1,
    'diligent_cost_rate': .4,
    'punishment_money_multiple': 10,
    'punishment_comment': .3 * merchant_par['comment_bound'],
    'whether_check_market': True,
    'check_with_weights': False,
    'prob_random_check': 0,
    'lazy': False,
    'prob_check_good': [1],
    'check_inside_market': True,
}

par_model_1_1 = {
    'mer': {
        'change_fake_rate': False,
        'comment_system': False,
    },
    'cus': {
        'buy_bound_change_real': 0,
        'buy_bound_change_fake': 0,
        'buy_comment_real': .5 * merchant_par['comment_bound'],
        'buy_comment_fake': .5 * merchant_par['comment_bound'],
        'prob_random_buy': 0,
    },
    'reg': {
        'whether_check_market': False
    },
}
default_par = copy.deepcopy({'mer': merchant_par, 'cus': customer_par, 'reg': regulator_par})
temp = update_par(default_par, par_model_1_1)
par_model_1_1 = temp

par_model_2_1 = copy.deepcopy(par_model_1_1)
par_model_2_1['cus'] = customer_par
par_model_2_1['mer']['comment_system'] = True
par_model_2_1['cus']['prob_comment_on_real'] = [1]
par_model_2_2 = copy.deepcopy(par_model_2_1)
par_model_2_2['cus']['prob_comment_on_real'] = [0.2]
par_model_2_3 = copy.deepcopy(par_model_2_2)
par_model_2_3['cus']['buy_with_weights'] = True
# par_model_2_3['reg']['check_with_weights']=True


par_model_3_1 = copy.deepcopy(par_model_2_1)
par_model_3_1['mer']['change_fake_rate'] = True
par_model_3_2 = copy.deepcopy(par_model_3_1)
par_model_3_2['cus']['prob_comment_on_real'] = [0.2]
par_model_3_3 = copy.deepcopy(par_model_3_2)
par_model_3_3['cus']['buy_with_weights'] = True
par_model_3_4 = copy.deepcopy(par_model_3_3)
par_model_3_4['cus']['identify_fake_rate'] = np.array([0.50])
par_model_3_5 = copy.deepcopy(par_model_3_3)
par_model_3_5['cus']['learning_fake_rate'] = 0.01

par_model_4_1 = copy.deepcopy(par_model_1_1)
par_model_4_1['cus'] = customer_par
par_model_4_1['reg']['whether_check_market'] = True
par_model_4_2 = copy.deepcopy(par_model_4_1)
par_model_4_2['reg']['punishment_money_multiple'] = 5
par_model_4_3 = copy.deepcopy(par_model_4_1)
par_model_4_3['reg']['punishment_money_multiple'] = 20

par_model_5_1 = copy.deepcopy(par_model_2_1)
par_model_5_1['reg']['whether_check_market'] = True
par_model_5_2 = copy.deepcopy(par_model_5_1)
par_model_5_2['cus']['prob_comment_on_real'] = [0.2]
par_model_5_3 = copy.deepcopy(par_model_5_2)
par_model_5_3['cus']['buy_with_weights'] = True
par_model_5_3['reg']['check_with_weights'] = True
par_model_5_4 = copy.deepcopy(par_model_5_3)
par_model_5_4['cus']['prob_random_buy'] = 0.5
par_model_5_4['reg']['prob_random_check'] = 0.5
par_model_5_5 = copy.deepcopy(par_model_5_4)
par_model_5_5['reg']['num'] = 1
par_model_5_6 = copy.deepcopy(par_model_5_5)
par_model_5_6['mer']['honest_num'] = 9
par_model_5_6['mer']['speculative_num'] = 1
par_model_5_7 = copy.deepcopy(par_model_5_5)
par_model_5_7['mer']['honest_num'] = 8
par_model_5_7['mer']['speculative_num'] = 2

par_model_6_1 = copy.deepcopy(par_model_5_1)
par_model_6_1['mer']['change_fake_rate'] = True
par_model_6_2 = copy.deepcopy(par_model_6_1)
par_model_6_2['cus']['prob_comment_on_real'] = [0.2]
par_model_6_3 = copy.deepcopy(par_model_6_2)
par_model_6_3['cus']['buy_with_weights'] = True
par_model_6_3['reg']['check_with_weights'] = True
par_model_6_4 = copy.deepcopy(par_model_6_3)
par_model_6_4['cus']['prob_random_buy'] = 0.5
par_model_6_4['reg']['prob_random_check'] = 0.5
par_model_6_5 = copy.deepcopy(par_model_6_4)
par_model_6_5['reg']['num'] = 1
par_model_6_5['mer']['honest_num'] = 5
par_model_6_5['mer']['speculative_num'] = 5
# par_model_6_5['reg']['lazy']=False
# par_model_6_5['cus']

par_model_7_1 = copy.deepcopy(par_model_6_5)
cus_change = {
    'prob_buy_good': [0.8, 0.2],
    'identify_fake_rate': np.array([0, 0.10]),
    'prob_comment_on_real': [0.2, 0.8],
    'buy_bound_change_real': [0.2, 0.6],
    'buy_bound_change_fake': [0.5, 1.5],
    'buy_comment_real': [10, 10],
    'buy_comment_fake': [5, 0],
}
par_model_7_1['cus'].update(cus_change)
mer_change = {
    'good_kind': [i for i in range(2)],
    'fake_cost': [0, 20],
    'fake_price': [0, 100],
    'real_cost': [5, 50],
    'real_price': [10, 100],
    'fake_rate': [0, 0.10],
    'decrease_fake_rate': np.array([0, 0.05]),
    'increase_fake_rate': np.array([0, 0.02]),
}
par_model_7_1['mer'].update(mer_change)
par_model_7_1['reg']['prob_check_good'] = [0.8, 0.2]
par_model_7_2 = copy.deepcopy(par_model_7_1)
par_model_7_2['reg']['num'] = 5

par_model_7_3 = copy.deepcopy(par_model_7_2)
par_model_7_3['mer'].update({'speculative_num': 1, 'honest_num': 9})

par_model_7_4 = copy.deepcopy(par_model_7_3)
par_model_7_4['reg']['num'] = 1

par_model_7_5 = copy.deepcopy(par_model_7_3)  # 5 reg
par_model_7_5['reg']['check_inside_market'] = False

par_model_7_6 = copy.deepcopy(par_model_7_4)  # 1 reg
par_model_7_6['reg']['check_inside_market'] = False

par_model_7_7 = copy.deepcopy(par_model_7_1)
par_model_7_7['reg']['check_inside_market'] = False
par_model_7_8 = copy.deepcopy(par_model_7_2)
par_model_7_8['reg']['check_inside_market'] = False

# par_model_7_9 = copy.deepcopy(par_model_7_1)
# par_model_7_9['reg']['check_inside_market'] = False
# par_model_7_9['mer'].update({'speculative_num': 9, 'honest_num': 1})
# par_model_7_10 = copy.deepcopy(par_model_7_2)
# par_model_7_10['reg']['check_inside_market'] = False
# par_model_7_10['mer'].update({'speculative_num': 9, 'honest_num': 1})

par_model_7_9 = copy.deepcopy(par_model_7_7)
par_model_7_9['reg']['prob_check_good'] = [0.5, 0.5]
par_model_7_10 = copy.deepcopy(par_model_7_8)
par_model_7_10['reg']['prob_check_good'] = [0.5, 0.5]
