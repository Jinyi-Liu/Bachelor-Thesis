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


pars = [parameter_no_review_no_regulator_no_change,
        parameter_no_review_with_regulator_no_change,
        parameter_with_review_no_regulator_no_change,
        parameter_with_review_with_regulator_no_change,
        parameter_with_review_no_regulator_with_change,
        parameter_with_review_with_regulator_with_change,
        parameter_with_review_with_regulator_with_change_with_random]
pars_titles = ['No Review No Regulator No Change',
               'No Review With Regulator No Change',
               'With Review No Regulator No Change',
               'With Review With Regulator No Change',
               'With Review No Regulator With Change',
               'With Review With Regulator With Change',
               'With Review With Regulator With Change With Random']
# pars = [parameter_with_review_with_regulator_with_change_with_random]
# pars_titles = ['With Review With Regulator With Change With Random']
pars=[parameter_with_review_with_regulator_with_change]
pars_titles=['test-3 regulator']
for (par, title) in zip(pars, pars_titles):
    merchants, customers, regulators = gen_models(regulators_num=3, **par)
    data, buy_data = game(game_rounds=1000, merchants=merchants, customers=customers, regulators=regulators)
    plot_image(data, title)
mer_profit = data[-1][2]
print(np.mean(mer_profit[-5:]) / np.mean(mer_profit[:5]))
print(np.mean(mer_profit[:5]) / np.mean(mer_profit[-5:]))
