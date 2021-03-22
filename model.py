import numpy as np
from random import seed, random, choice

seed(1)
comment_bound = 10


class Merchant:
    def __init__(self, par):
        self.ID = par[0]
        self.comment = par[1][0]
        self.comment_count = par[1][1]

        self.good_kind = par[2]

        self.fake_rate = np.array(par[3])

        self.fake_cost = par[4][0]
        self.fake_price = par[4][1]
        self.real_cost = par[5][0]
        self.real_price = par[5][1]

        self.de_fake_bound = par[6][0]  # If the comment hit the bound, then the merchant will decrease the fake rate
        self.de_fake_rate = par[6][1]
        self.in_fake_bound = par[6][2]  # When the bound is approached, the opportunistic merchant will increase the
        # fake rate.
        self.in_fake_rate = par[6][3]
        self.sell_count = 0  # times the merchant sells goods.
        self.punished_count = 0  # how many times the merchant be punished
        self.money = 0

    def fake_change(self):
        if self.comment < self.de_fake_bound:
            self.fake_rate *= self.de_fake_rate
        elif self.comment > self.in_fake_bound:
            self.fake_rate *= self.in_fake_rate
            self.fake_rate[self.fake_rate >= 1] = 1

    def punished(self):
        pass

    def adjust_comment(self):
        if self.comment < 0:
            self.comment = 0
        if self.comment > comment_bound:
            self.comment = comment_bound


class Customer:
    def __init__(self, par):
        self.ID = par[0]
        self.buy_bound = par[1]
        self.identify_fake_rate = par[2]
        self.buy_bound_real = par[3][0]
        self.buy_bound_fake = par[3][1]
        self.buy_comment_real = par[4][0]  # After buying something, the comment customer makes.
        self.buy_comment_fake = par[4][1]
        self.prob_random = par[5]  # Irrational customer.
        #  Parameter TBD

    def change_bound(self, perceive_real=None):
        """
        Change the buy_bound if bought something genuine or fake.
        Need some changes on the bound changing process, e.g., functional change?
        :param perceive_real:
        :return:
        """
        if perceive_real:
            self.buy_bound -= self.buy_bound_real
        else:
            self.buy_bound += self.buy_bound_fake
        if self.buy_bound < 0:
            self.buy_bound = 0
        elif self.buy_bound > 10:
            self.buy_bound = 10

    def random_buy(self):
        """
        Irrational in this round. Buy something randomly without considering his/her bound for goods.
        :return:
        """
        pass

    def buy(self, mers, mers_num):
        """
        Act.
        :param mers: from _mers to choose someone to buy
        :param mers_num:
        :return:
        """
        index, mers = bound_choose(mers, mers_num, self.buy_bound)  # buying with consideration of the bound.
        index = random_choose(index, mers_num, self.prob_random)  # irrational: randomly choose someone to buy.
        if index == 0:  # No merchant to buy.
            return -1, None, None
        merchant2buy = choice(mers[:index])
        good_kind = choice(merchant2buy.good_kind)
        fake_rate = merchant2buy.fake_rate[good_kind-1]
        identify_fake_rate = self.identify_fake_rate[good_kind-1]  # rate for identifying such good
        rand = random()
        perceive_type = True  # Customer's thought
        true_type = True  # Goods real type
        # sold fake and identified to be fake.
        if rand <= fake_rate * identify_fake_rate:
            self.change_bound(False)
            true_type = False
            perceive_type = False
        # Merchant sold fake but wasn't found by the customer.
        if fake_rate * identify_fake_rate < rand <= fake_rate:
            self.change_bound(True)
            true_type = False
            perceive_type = True
        else:
            # Sold real
            # Default
            self.change_bound(True)
        merchant2buy.money += revenue(true_type, good_kind, merchant2buy)
        merchant2buy.sell_count += 1
        return perceive_type, merchant2buy.ID, good_kind


class Regulator:
    def __init__(self, par):
        """

        :param par:
        """
        self.ID = par[0]
        self.lazy_i_rate = par[1][0]  # Lazily regulate.
        self.lazy_cost_rate = par[1][1]
        self.diligent_i_rate = par[2][0]  # The ability to spot the fake when diligently regulate the market.
        self.diligent_cost_rate = par[2][1]
        self.punishment_money_multiple = par[3][0]
        self.punishment_comment_multiple = par[3][1]
        self.fine_got = 0
        self.check_cost = 0
        # self.make_public = True

    def check_market(self, lazy=None, mers=None, ):
        """
        To check the market.
        :return:
        """
        merchant2check = choice(mers)
        good2check = choice(merchant2check.good_kind)
        fake_rate = merchant2check.fake_rate[good2check]
        rand = random()
        if lazy:
            # Merchant sold fake good and was caught.
            if rand <= fake_rate * self.lazy_i_rate:
                self.punish(True, merchant2check)
                # TBD
        else:
            if rand <= fake_rate * self.diligent_i_rate:
                self.punish(False, merchant2check)
                # TBD

    def punish(self, good_price=None, lazy=None, mer=None):
        mer.punished_count += 1
        mer.money -= self.punishment_money_multiple * good_price
        mer.comment -= self.punishment_comment_multiple * comment_bound
        self.fine_got += self.punishment_money
        self.check_cost += good_price * (self.lazy_cost_rate if lazy else self.diligent_cost_rate)

    def make_public(self):
        pass


def random_choose(index, mers_num, p_random):
    """
    if random()>p_random, i.e., not randomly choose who to buy.
    :param index: chose by bound_choose
    :param mers_num: overall mers' number
    :param p_random: prob one randomly buy something
    :return:
    """
    if random() > p_random:
        return index
    else:
        return mers_num


def bound_choose(mers, mers_num, bound):
    _mer = sorted(mers, key=lambda x: x.comment, reverse=True)
    _iter = filter(lambda x: x.comment < bound, _mer)
    try:
        index = _mer.index(next(_iter))
    except StopIteration:
        index = mers_num
    return index, _mer


def revenue(real=None, good_kind=None, merchant2buy=None):
    good_kind = good_kind-1
    if not real:
        price = merchant2buy.fake_price[good_kind]
        cost = merchant2buy.fake_cost[good_kind]
    else:
        price = merchant2buy.real_price[good_kind]
        cost = merchant2buy.real_cost[good_kind]
    return price - cost
