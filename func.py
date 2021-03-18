# -*- coding: utf-8 -*-
from model import *
from math import exp
X = 10
fake_margin = 0.2
real_margin = 0.5
fake_price_efficiency = 0.9  # TBD! a function of price

# Merchant's default parameter
_comment = 5
_good_kind = [x for x in range(X)]  # how many goods one merchant sells
_fake_rate = None  #
_fake_c_par = [fake_margin * exp(i) for i in _good_kind]  # fake_cost
_fake_p_par = [fake_price_efficiency*exp(i) for i in _good_kind]  # fake_price
_real_c_par = [real_margin * exp(i) for i in _good_kind]  # real_cost
_real_p_par = [exp(i) for i in _good_kind]  # real_price
_bound_par = [3, 0.05, 9, 0.05]  # de_fake_bound & rate, in_fake_bound & rate

# Customer's default parameter
_buy_bound = 5
_identify_fake_rate = 0
_buy_bound_par = []  # buy_bound_incr & decr
_buy_comment_par = []  # buy_comment_incr & decr
_prob_random = None  # the probability that one buys something randomly

# Regulator's default parameter
_lazy_par = []  # lazy_fake_rate; lazy_cost
_diligent_par = []  # diligent_fake_rate, diligent_cost
_punishment_par = []  # punishment_money, punishment_comment


def gen_mer_model(mer_id=None, comment=_comment, good_kind=_good_kind, fake_rate=_fake_rate, fake_c_par=_fake_c_par,
                  fake_p_par = _fake_p_par,real_c_par=_real_c_par, real_p_par=_real_p_par, bound_par=_bound_par):
    par = [mer_id, comment, good_kind, fake_rate, fake_c_par,fake_p_par, real_c_par,real_p_par, bound_par]
    mer = Merchant(par)
    return mer


def gen_cus_model(cus_id=None, buy_bound=_buy_bound, identify_fake_rate=_identify_fake_rate, buy_bound_par=_buy_bound_par,
                  buy_comment_par=_buy_comment_par, prob_random=_prob_random):
    par = [cus_id, buy_bound, identify_fake_rate, buy_bound_par, buy_comment_par, prob_random]
    cus = Customer(par)
    return cus


def gen_regulator_model(reg_id=None, lazy_par=_lazy_par, diligent_par=_diligent_par, punishment_par=_punishment_par):
    par = [reg_id, lazy_par, diligent_par, punishment_par]
    regulator = Regulator(par)
    return regulator

def gen_models():
    pass


def game(merchants, customers, regulators):


    pass
