import locale

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
dips_id = []
fuel_id = []
purchases_id = []
top_id = []
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


try:
    args = hselect("name", "subaccounts", "", "")
    arg = hselect("name", "sub_subaccounts", "", "")
    arr = args + arg
    for n in range(0, len(arr), 1):
        t = arr[n][0].lower() + "_id"
        globals()[t] = []
except IndexError:
    print("c")


def sales_litres(index=0, product="product", opening_stock=0, closing_stock=0, rtt=0):
    opening_stock = float(opening_stock)
    closing_stock = float(closing_stock)
    rtt = float(rtt)
    real_insert(pro, index, product)
    real_insert(op, index, opening_stock)
    real_insert(cl, index, closing_stock)
    real_insert(rt, index, rtt)
    try:
        field = "product='" + pro[index] + "', " + "opening_meter='" + str(op[index]) + "'," \
                + "closing_meter='" + str(cl[index]) + "'," + \
                "rtt='" + str(rt[index]) + "'"
        condition = "fuelid=" + str(fuel_id[index])
        hupdate("fuel", field, condition)
    except IndexError:
        insert_id = hselect("Max(id)", "fuel", "", "")[0][0]
        insert_id += 1
        hinsert("fuel", insert_id, branch_id[0], str(sales_date[0]), pro[index],
                op[index], cl[index], rt[index])
        real_insert(fuel_id, index, insert_id)
    return str(closing_stock - (opening_stock + rtt))


def sales_shs(index=0, litres=0, price=0):
    price = int(price)
    litres = float(litres)
    real_insert(pr, index, price)

    real_insert(amount_array, index, litres * price)
    return amount_array[index], add_array(amount_array, index)


def dips(pms_od=0, pms_cd=0, ago_od=0, ago_cd=0, bik_od=0, bik_cd=0):
    pms_od = float(pms_od)
    pms_cd = float(pms_cd)
    ago_od = float(ago_od)
    ago_cd = float(ago_cd)
    bik_od = float(bik_od)
    bik_cd = float(bik_cd)

    try:
        field = "pms_od='" + str(pms_od) + "',pms_cd='" + str(pms_cd) + "',ago_od='" + str(ago_od) + \
                "',ago_cd='" + str(ago_cd) + "',bik_od='" + str(bik_od) + "',bik_cd='" + str(bik_cd) + "'"
        condition = "id=" + str(dips_id[0])
        hupdate("dips", field, condition)
    except IndexError:
        insert_id = hselect("Max(id)", "dips", "", "")[0][0]
        insert_id += 1
        hinsert("dips", insert_id, branch_id[0], str(sales_date[0]),
                pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd)
        real_insert(dips_id, 0, insert_id)
    return pms_od - pms_cd, ago_od - ago_cd, bik_od - bik_cd


def insertion(arr, table, index, details, debit, credit):
    debit = float(debit)
    credit = float(credit)
    real_insert(details_array, index, details)
    real_insert(debit_array, index, debit)
    real_insert(credit_array, index, credit)
    try:
        field = "details='{0}', debit='{1}', credit='{2}'".format(details_array[index],
                                                                  str(debit_array[index]),
                                                                  str(credit_array[index]))

        condition = "id={0}".format(str(arr[index]))
        hupdate(table, field, condition)
    except IndexError:
        insert_id = hselect("Max(id)", table, "", "")[0][0]
        if insert_id is None:
            insert_id = 0
        insert_id += 1
        hinsert(table, insert_id, str(sales_date[0]), branch_id[0],
                details_array[index], debit_array[index], credit_array[index])
        real_insert(arr, index, insert_id)

    return str(add_array(debit_array, index)), str(add_array(credit_array, index))


def login(user, password):
    users = " WHERE username=" + "'" + user + "' "
    passwords = "AND password='" + password + "'"
    result = hselect(operation="id, username,pumps", table="users", condition1=users, condition2=passwords)
    if result:
        real_insert(branch_id, 0, result[0][0])
        return result[0][1], result[0][2]
    else:
        return 0


def get_details():
    sales = get_data("fuel", fuel_id)
    return sales


def get_data(table, arr):
    result = hselect("*", table, " WHERE branchid=" + str(branch_id[0]),
                     " AND date='" + sales_date[0] + "'")
    print(result)
    for i in range(0, len(result), 1):
        real_insert(arr, i, result[i][0])
    return result


def add_array(args, index):
    total = 0
    index += 1
    for a in args[:index]:
        total += a
    return total


def fuel_purchase(pms, pms_price, ago, ago_price, bik, bik_price):
    pms = int(pms)
    pms_price = float(pms_price)
    ago = int(ago)
    ago_price = float(ago_price)
    bik = int(bik)
    bik_price = float(bik_price)

    try:
        field = "pms='" + str(pms) + "',pms_price='" + str(pms_price) + \
                "',ago='" + str(ago) + \
                "',ago_price='" + str(ago_price) + \
                "',bik='" + str(bik) + "',bik_price='" + str(bik_price) + "'"
        condition = "id=" + str(purchases_id[0])
        hupdate("fuel_purchases", field, condition)
    except IndexError:
        insert_id = hselect("Max(id)", "fuel_purchases", "", "")[0][0]
        insert_id += 1
        hinsert("fuel_purchases", insert_id, str(sales_date[0]), branch_id[0],
                pms, pms_price, ago, ago_price, bik, bik_price)
        real_insert(purchases_id, 0, insert_id)


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
