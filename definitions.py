import locale
import sqlite3

from database_handler import *

branch_id = []
pro = []
op = []
cl = []
rt = []
pr = []
al = []
amount_array = []
sales_date = []
details_array = []
debit_array = []
credit_array = []
assets_id = []
liabilities_id = []
expenses_id = []
incomes_id = []
arrays = []


def real_insert(arr, index, value):
    try:
        arr[index] = value
    except IndexError:
        arr.insert(index, value)


def sales_litres(product_id=0, product="product", opening_stock=0, closing_stock=0, rtt=0):
    opening_stock = float(opening_stock)
    closing_stock = float(closing_stock)
    rtt = float(rtt)
    if product_id:
        field = "product='{0}', opening_meter={1},closing_meter={2}," \
                "rtt={3}".format(product, opening_stock, closing_stock, rtt)
        hupdate("fuel", field, "fuelid={0}".format(product_id))
        insert_id = product_id
    else:
        insert_id = hinsert("fuel", "branchid, date, product, opening_meter, closing_meter, rtt",
                            branch_id[0], str(sales_date[0]), product, opening_stock, closing_stock, rtt)
    return str(closing_stock - (opening_stock + rtt)), insert_id


def sales_shs(index=0, litres=0, price=0):
    price = int(price)
    litres = float(litres)
    real_insert(pr, index, price)

    real_insert(amount_array, index, litres * price)
    return amount_array[index], add_array(amount_array, index)


def dips(dips_id, pms_od=0, pms_cd=0, ago_od=0, ago_cd=0, bik_od=0, bik_cd=0):
    pms_od = float(pms_od)
    pms_cd = float(pms_cd)
    ago_od = float(ago_od)
    ago_cd = float(ago_cd)
    bik_od = float(bik_od)
    bik_cd = float(bik_cd)

    try:
        field = "pms_od={0},pms_cd={1},ago_od={2}," \
                "ago_cd={3},bik_od={4}," \
                "bik_cd={5}".format(pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd)

        hupdate("dips", field, "id={0}".format(dips_id))
        insert_id = dips_id
    except sqlite3.OperationalError:
        insert_id = hinsert("dips", "branchid, date, pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd",
                            branch_id[0], str(sales_date[0]),
                            pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd)
    return str(pms_od - pms_cd), str(ago_od - ago_cd), str(bik_od - bik_cd), insert_id


def insertion(table, position, index, details, debit, credit):
    debit = float(debit)
    credit = float(credit)
    real_insert(details_array, index, details)
    real_insert(debit_array, index, debit)
    real_insert(credit_array, index, credit)

    try:
        field = "details='{0}', debit={1}, credit={2}".format(details_array[index],
                                                              debit_array[index],
                                                              credit_array[index])
        hupdate(table, field, "id={0}".format(position))
        insert_id = position
    except sqlite3.OperationalError:
        insert_id = hinsert(table, "date, branchid, details, debit, credit", str(sales_date[0]), branch_id[0],
                            details_array[index], debit_array[index], credit_array[index])
    return str(add_array(debit_array, index)), str(add_array(credit_array, index)), insert_id


def login(user, password):
    users = " WHERE username=" + "'" + user + "' "
    passwords = "AND password='" + password + "'"
    result = hselect(operation="id, username,pumps", table="users", condition1=users, condition2=passwords)
    if result:
        real_insert(branch_id, 0, result[0][0])
        return result[0][1], result[0][2]
    else:
        return 0


def get_data(table):
    result = hselect("*", table, " WHERE branchid=" + str(branch_id[0]),
                     " AND date='" + sales_date[0] + "'")
    return result


def add_array(args, index):
    total = 0
    index += 1
    for a in args[:index]:
        total += a
    return total


def fuel_purchase(index, pms, pms_price, ago, ago_price, bik, bik_price):
    pms = int(pms)
    pms_price = float(pms_price)
    ago = int(ago)
    ago_price = float(ago_price)
    bik = int(bik)
    bik_price = float(bik_price)

    try:
        field = "pms={0},pms_price={1},ago={2},ago_price={3}," \
                "bik={4},bik_price={5}".format(pms, pms_price, ago, ago_price, bik, bik_price)
        hupdate("fuel_purchases", field, "id={0}".format(index))
        insert_id = index
    except sqlite3.OperationalError:
        insert_id = hinsert("fuel_purchases", "date, branchid, pms, pms_price, ago, ago_price, bik, bik_price",
                            str(sales_date[0]), branch_id[0],
                            pms, pms_price, ago, ago_price, bik, bik_price)
    return insert_id


def thousand_separator(data):
    if data is not None:
        try:
            d = float(data)
            return locale.format("%d", d, grouping=True)
        except ValueError:
            return str(0)


def cashbook():
    return hselect("*", "cashbook", " WHERE branchid={0}".format(str(branch_id[0])), "")


def trial():
    return hselect("*", "trial", " WHERE branchid={0}".format(str(branch_id[0])),
                   " AND date={0}".format(str(sales_date[0])))
