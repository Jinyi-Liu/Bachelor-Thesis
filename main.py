from func import *

#mers, cus, regs=gen_models()
# buy_data = [perceive_type, mer2buy_id, good_kind, true_type]
cus_change_par = {}
reg_change_par = {}
mer_change_par = {}
change_par = {
    'cus': cus_change_par,
    'reg': reg_change_par,
    'mer': mer_change_par
}
data, buy_data = game(**change_par)
plot_image(data)