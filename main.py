from func import *
from _plot import *
from default_par import *
from random import seed
import pickle

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


# pars = [parameter_no_review_no_regulator_no_change,
#         parameter_no_review_with_regulator_no_change,
#         parameter_with_review_no_regulator_no_change,
#         parameter_with_review_with_regulator_no_change,
#         parameter_with_review_no_regulator_with_change,
#         parameter_with_review_with_regulator_with_change,
#         parameter_with_review_with_regulator_with_change_with_random]
# pars_titles = ['No Review No Regulator No Change',
#                'No Review With Regulator No Change',
#                'With Review No Regulator No Change',
#                'With Review With Regulator No Change',
#                'With Review No Regulator With Change',
#                'With Review With Regulator With Change',
#                'With Review With Regulator With Change With Random']
# pars = [parameter_with_review_with_regulator_with_change_with_random]
# pars_titles = ['With Review With Regulator With Change With Random']

# pars = [par_model_2_1, par_model_2_2,par_model_2_3]
# pars_titles = ['model_2-1', 'model_2-2','model_2-3']

# pars = [par_model_3_1, par_model_3_2,par_model_3_3]
# pars_titles = ['model_3-1', 'model_3-2','model_3-3']

# pars = [par_model_4_1, par_model_4_2, par_model_4_3]
# pars_titles = ['model_4-1', 'model_4-2', 'model_4-3']
"""
pars_new = []
for par in pars:
    q = copy.deepcopy(par)
    q['mer']['honest_num'] = 9
    q['mer']['speculative_num'] = 1
    pars_new.append(q)
pars_titles_new = [j[:-1]+'%d'%(4+i) for i, j in enumerate(pars_titles)]
times = 10
for par, title in zip(pars_new, pars_titles_new):
    monte_process_data(par, title, times)
plot_image_4(pars_titles_new, show=0)
"""
# pars = [par_model_5_1, par_model_5_2, par_model_5_3,par_model_5_4]
# pars_titles = ['model_5-1', 'model_5-2', 'model_5-3', 'model_5-4']
# pars = [par_model_5_5]
# pars_titles= ['model_5-5']

# pars = [par_model_5_7]
# pars_titles= ['model_5-7']

# pars = [par_model_6_1, par_model_6_2,par_model_6_3,par_model_6_4,par_model_6_5]
# pars_titles = ['model_6-1', 'model_6-2','model_6-3','model_6-4','model_6-5']

pars = [par_model_7_9,par_model_7_10]
pars_titles = ['model_7-9','model_7-10']

# pars = [par_model_7_1, par_model_7_2,par_model_7_3,par_model_7_4]
# pars_titles = ['model_7-1', 'model_7-2','monte_7-3','monte_7-4']
# pars = [par_model_7_5,par_model_7_6]
# pars_titles = ['model_7-5','model_7-6']
# pars = [par_model_7_7,par_model_7_8]
# pars_titles = ['model_7-7','model_7-8']
# pars = [par_model_7_9,par_model_7_10]
# pars_titles = ['model_7-9','model_7-10']
show = False
# output_single(pars, pars_titles, show=show, set_seed=2)

# times = 30
# for par, title in zip(pars, pars_titles):
#     monte_process_data(par, title, times)
#     plot_monte_average(title, show=show, times=times)
#     plot_monte_all(title, show=show, times=times)
pars_titles = ['model_7-8','model_7-10']
plot_monte_average_all(pars_titles,False,times)
# plot_reg_cost(pars_titles,times)
# plot_image_5(pars_titles[2:], show=False)
