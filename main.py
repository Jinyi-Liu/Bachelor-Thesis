from func import *
from default_par import *

general_change_par = {}
cus_change_par = {}
reg_change_par = {}
mer_change_par = {}


def gen_change_par(_general_change_par={}, _cus_change_par={}, _reg_change_par={}, _mer_change_par={}):
    _change_par = {
        'general': _general_change_par,
        'cus': _cus_change_par,
        'reg': _reg_change_par,
        'mer': _mer_change_par
    }
    return _change_par


"""
# cus_change_par['identify_fake_rate'] = [0.6, 0.3, 0.15, 0.3]
mer_change_par['change_fake_rate'] = False
cus_change_par['identify_fake_rate'] = [1., 1., 1., 1.]
cus_change_par['prob_random_buy'] = 0.2
change_par = gen_change_par({}, cus_change_par, reg_change_par, mer_change_par)
# merchants, customers, regulators = gen_models(**change_par)
"""
#par_set = [parameter_no_review_no_regulator, parameter_no_review_with_regulator, parameter_with_review_no_regulator,
#           parameter_with_review_with_regulator]
for par in [parameter_with_review_with_regulator_with_change]:
    merchants, customers, regulators = gen_models(**par)
    data, buy_data = game(game_rounds=5000, merchants=merchants, customers=customers, regulators=regulators)
    plot_image(data, )
mer_profit = data[-1][2]
np.mean(mer_profit[-5:])/np.mean(mer_profit[:5])
np.mean(mer_profit[:5])/np.mean(mer_profit[-5:])