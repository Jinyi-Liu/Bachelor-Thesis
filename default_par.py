import numpy as np

# Global parameters
general_par = {
    'total_good_kinds': 4,
    'fake_margin': 0.2,
    "real_margin": 0.5,
    "fake_price_efficiency": 0.9,
    'fake_rate_lower_bound': 0.01,
    'fake_rate_upper_bound': 0.5,
}

# Merchant's default parameter
good_kind = [x for x in range(general_par['total_good_kinds'])]
real_p_par = [10, 100, 500, 5000]  # real_price
real_c_par = [general_par['real_margin'] * price for price in real_p_par]  # real_cost
fake_p_par = [general_par['fake_price_efficiency'] * price for price in real_p_par]  # fake_price
fake_c_par = [general_par['fake_margin'] * fake_price for fake_price in fake_p_par]  # fake_cost

merchant_par = {
    'comment': 5,
    'comment_bound': 10,
    'comment_count': 0,
    'good_kind': good_kind,
    'fake_rate': np.array([.50, .30, .10, .05]),
    'fake_rate_lower_bound': 0,
    'fake_rate_upper_bound': 0.5,
    'fake_price': fake_p_par,
    'fake_cost': fake_c_par,
    'real_price': real_p_par,
    'real_cost': real_c_par,
    'decrease_fake_bound': 3,
    'decrease_fake_rate': 0.05,
    'increase_fake_bound': 8,
    'increase_fake_rate': 0.02,
    'honest': False
}

# Customer's default parameter
customer_par = {
    'buy_bound': 5,
    'buy_good_prob': [0.4, 0.3, 0.2, 0.1],
    'identify_fake_rate': [0.05, 0.1, 0.15, 0.3],
    'buy_bound_change_real': 0.2,
    'buy_bound_change_fake': 0.5,
    'buy_comment_real': 1 * merchant_par['comment_bound'],
    'buy_comment_fake': .5 * merchant_par['comment_bound'],
    'prob_random_buy': 0.1
}

# Regulator's default parameter
regulator_par = {
    'lazy_identify_rate': .8,
    'lazy_cost_rate': .2,
    'diligent_identify_rate': 1,
    'diligent_cost_rate': .4,
    'punishment_money_multiple': 10,
    'punishment_comment': .3 * merchant_par['comment_bound'],
    'whether_check_market': True
}

parameter_no_review_no_regulator = {
    'mer': {
        'change_fake_rate': False,
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

parameter_no_review_with_regulator = {
    'mer': {
        'change_fake_rate': False,
    },
    'cus': {
        'buy_bound_change_real': 0,
        'buy_bound_change_fake': 0,
        'buy_comment_real': .5 * merchant_par['comment_bound'],
        'buy_comment_fake': .5 * merchant_par['comment_bound'],
        'prob_random_buy': 0,
    },
    'reg': {
        'whether_check_market': True
    },
}

parameter_with_review_no_regulator = {
    'mer': {
        'change_fake_rate': True,
    },
    'cus': {
        'buy_bound_change_real': .2,
        'buy_bound_change_fake': 2,
        'buy_comment_real': 1 * merchant_par['comment_bound'],
        'buy_comment_fake': .2 * merchant_par['comment_bound'],
        'prob_random_buy': 0,
    },
    'reg': {
        'whether_check_market': False
    },
}

parameter_with_review_with_regulator = {
    'mer': {
        'change_fake_rate': True,
    },
    'cus': {
        'buy_bound_change_real': .2,
        'buy_bound_change_fake': 2,
        'buy_comment_real': 1 * merchant_par['comment_bound'],
        'buy_comment_fake': .2 * merchant_par['comment_bound'],
        'prob_random_buy': 0,
    },
    'reg': {
        'whether_check_market': True
    },
}
