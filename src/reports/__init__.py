#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is Copyright (C) 2017, Paul Lutus
# and is released under the GPL:
# https://www.gnu.org/licenses/gpl-3.0.en.html
from piecash import open_book

balance = 0


def recurse(node, tab=''):
    global balance
    balance += node.get_balance()
    print("%-80s : %12.2f : %12.2f" % ("%s%s" % (tab, str(node)), node.get_balance(), balance))
    for child in node.children:
        recurse(child, tab + '  ')


def get_balance(self, recurse=True, commodity=None):
    """
    Returns the balance of the account (including its children accounts if recurse=True)
    expressed in account's commodity/currency.
    If this is a stock/fund account, it will return the number of shares held.
    If this is a currency account, it will be in account's currency.
    In case of recursion, the commodity of children accounts will be transformed to the commodity of the father account using the latest price
    (if no price is available to convert , it is considered as 0)

    Attributes:
        recurse (bool, optional): True if the balance should include children accounts (default to True)
        commodity (:class:`piecash.core.commodity.Commodity`): the currency into which to get the balance (default to None, i.e. the currency of the account)

    Returns:
        the balance of the account
    """
    if commodity is None:
        commodity = self.commodity
    balance = sum([sp.quantity for sp in self.splits]) * self.sign

    if recurse and self.children:
        balance += sum(acc.get_balance(recurse=recurse, commodity=commodity) for acc in self.children)

    return balance


# change this path to suit your needs
data_path = '/root/Desktop/kk.gnucash'
with open_book(data_path) as book:
    recurse(book.root_account)
