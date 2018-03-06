from definitions import *

total_assets = 0
current_assets = []
fixed_assets = []


def Capital(total_assts, total_lias):
    return total_assts - total_lias


def total_assets():
    total_assets = add_array(current_assets + fixed_assets)
