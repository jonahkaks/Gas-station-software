import locale

from database_handler import *

pro = []
op = []
cl = []
rt = []
pr = []
expn = []
expa = []
lubn = []
luba = []
send = []
withdraw = []
fuelname = []
prepname = []
prepamount = []
debtorn = []
paid = []
taken = []
amount_array = []
branch_id = [1]
sales_date = []
lubid = []
expid = []
dips_id = []
debtor_id = []
fuel_id = []
prepaid_id = []
airtels = []
airtelw = []
mtns = []
mtnw = []
mobile_id = []
cash_id = []
cashed = []
banked = []
purchases = []


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
        insert_id = hselect("count(*)", "fuel", "", "")[0][0]
        insert_id += 1
        hinsert("fuel", insert_id, branch_id[0], str(sales_date[0]), pro[index],
                op[index], cl[index], rt[index])
        real_insert(fuel_id, index, insert_id)
    return str(closing_stock - (opening_stock + rtt))


def sales_shs(index=0, litres=0, price=0):
    price = int(price)
    litres = float(litres)
    real_insert(pr, index, price)
    amount = litres * price
    real_insert(amount_array, index, int(amount))
    total = add_array(amount_array, index)
    return locale.format("%d", amount, grouping=True), locale.format("%d", total, grouping=True)


def expenses(index=0, exp_name="expense", exp_amount=0):
    exp_amount = int(exp_amount)
    real_insert(expn, index, exp_name)
    real_insert(expa, index, exp_amount)
    try:
        field = "name='" + expn[index] + "'," + "amount='" + str(expa[index]) + "'"
        condition = "id=" + str(expid[index])
        hupdate("expenses", field, condition)
    except IndexError:
        insert_id = hselect("count(*)", "expenses", "", "")[0][0]
        insert_id += 1
        hinsert("expenses", insert_id, branch_id[0], str(sales_date[0]),
                expn[index], expa[index])
        real_insert(expid, index, insert_id)
    total = add_array(expa, index)
    return locale.format("%d", total, grouping=True)


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
        insert_id = hselect("count(*)", "dips", "", "")[0][0]
        insert_id += 1
        hinsert("dips", insert_id, branch_id[0], str(sales_date[0]),
                pms_od, pms_cd, ago_od, ago_cd, bik_od, bik_cd)
        real_insert(dips_id, 0, insert_id)
    return pms_od - pms_cd, ago_od - ago_cd, bik_od - bik_cd


def lubricants(index=0, lub_name="lubricants", lub_amount=0):
    lub_amount = int(lub_amount)
    real_insert(lubn, index, lub_name)
    real_insert(luba, index, lub_amount)
    try:
        field = "name='" + lubn[index] + "'," + "amount='" + str(luba[index]) + "'"
        condition = "id=" + str(lubid[index])
        hupdate("lubricants", field, condition)
    except IndexError:
        insert_id = hselect("count(*)", "lubricants", "", "")[0][0]
        insert_id += 1
        hinsert("lubricants", insert_id, str(sales_date[0]), branch_id[0],
                lubn[index], luba[index])
        real_insert(lubid, index, insert_id)
    total = add_array(luba, index)
    return locale.format("%d", total, grouping=True)


def prepaid(index=0, prepaid_name="prep", prepaid_amount=0):
    if len(prepaid_name) and len(prepaid_amount) > 0:
        prepaid_amount = int(prepaid_amount)
        real_insert(prepname, index, prepaid_name)
        real_insert(prepamount, index, prepaid_amount)
        try:
            field = "name='" + prepname[index] + "'," + "amount='" \
                    + str(prepamount[index]) + "'"
            condition = "id=" + str(prepaid_id[index])
            hupdate("prepaid", field, condition)
        except IndexError:
            insert_id = hselect("count(*)", "prepaid", "", "")[0][0]
            insert_id += 1
            hinsert("prepaid", insert_id, str(sales_date[0]), branch_id[0],
                    prepname[index], prepamount[index])
            real_insert(prepaid_id, index, insert_id)
        total = add_array(prepamount, index)
        return locale.format("%d", total, grouping=True)


def debtors(index=0, debtor="name", debt_taken=0, debt_paid=0):
    debt_paid = int(debt_paid)
    debt_taken = int(debt_taken)
    real_insert(debtorn, index, debtor)
    real_insert(taken, index, debt_taken)
    real_insert(paid, index, debt_paid)
    try:
        field = "name='" + debtorn[index] + "'," + "taken='" + str(taken[index]) + "'," + "paid='" + str(
            paid[index]) + "'"
        condition = "id=" + str(debtor_id[index])
        hupdate("debtors", field, condition)
    except IndexError:
        insert_id = hselect("count(*)", "debtors", "", "")[0][0]
        insert_id += 1
        hinsert("debtors", insert_id, str(sales_date[0]), branch_id[0], debtorn[index],
                taken[index], paid[index])
        real_insert(debtor_id, index, insert_id)
    total1, total2 = add_array(paid, index), add_array(taken, index)
    return locale.format("%d", total1, grouping=True), locale.format("%d", total2, grouping=True)


def login(user, password):
    users = " WHERE username=" + "'" + user + "' "
    passwords = "AND password='" + password + "'"
    result = hselect(operation="id, username,pumps", table="users", condition1=users, condition2=passwords)
    if result:
        real_insert(branch_id, 0, result[0][0])
        return result[0][1], result[0][2]
    else:
        return 0


def cancel(table):
    hdelete(table, sales_date[0])


def get_details():
    sales = get_data("fuel", fuel_id)
    mobile = get_data("mobile", mobile_id)
    prep = get_data("prepaid", prepaid_id)
    expense = get_data("expenses", expid)
    debtor = get_data("debtors", debtor_id)
    lubricant = get_data("lubricants", lubid)
    dips = get_data("dips", dips_id)
    cash = get_data("cash", cash_id)
    fuel = get_data("fuel_purchases", purchases)
    return sales, mobile, prep, expense, debtor, lubricant, dips, cash, fuel


def get_data(table, arr):
    result = hselect("*", table, " WHERE branchid=" + str(branch_id[0]),
                     " AND date='" + sales_date[0] + "'")
    for i in range(0, len(result), 1):
        real_insert(arr, i, result[i][0])
    return result


def mobile_money(index, airtel_sending, airtel_withdraw, mtn_sending, mtn_withdraw):
    real_insert(airtels, index, airtel_sending)
    real_insert(airtelw, index, airtel_withdraw)
    real_insert(mtns, index, mtn_sending)
    real_insert(mtnw, index, mtn_withdraw)

    try:
        field = "airtel_sending='" + airtels[index] + "'," + "airtel_withdraw='" + str(
            airtelw[index]) + "'," + "mtn_sending='" + str(mtns[index]) + "'," + "mtn_withdraw='" + str(
            mtnw[index]) + "'"
        condition = "id=" + str(mobile_id[index])
        hupdate("mobile", field, condition)
    except IndexError:
        insert_id = hselect("count(*)", "mobile", "", "")[0][0]
        insert_id += 1
        hinsert("mobile", insert_id, str(sales_date[0]), branch_id[0], airtels[index],
                airtelw[index], mtns[index], mtnw[index])
        real_insert(mobile_id, index, insert_id)


def cash(index, cash, bank):
    real_insert(cashed, index, cash)
    real_insert(banked, index, bank)
    try:
        field = "cash='" + cashed[index] + "'," + "banked='" + banked[index] + "'"
        condition = "id=" + str(cash_id[index])
        hupdate("cash", field, condition)
    except IndexError:
        insert_id = hselect("count(*)", "cash", "", "")[0][0]
        insert_id += 1
        hinsert("cash", insert_id, branch_id[0], str(sales_date[0]), cashed[index], banked[index])
        real_insert(cash_id, index, insert_id)


def add_array(args, index):
    total = 0
    index += 1
    for a in args[:index]:
        total += a
    return total


def real_insert(arr, index, value):
    try:
        arr[index] = value
    except IndexError:
        arr.insert(index, value)


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
        condition = "id=" + str(purchases[0])
        hupdate("fuel_purchases", field, condition)
    except IndexError:
        insert_id = hselect("count(*)", "fuel_purchases", "", "")[0][0]
        insert_id += 1
        hinsert("fuel_purchases", insert_id, branch_id[0], str(sales_date[0]),
                pms, pms_price, ago, ago_price, bik, bik_price)
        real_insert(purchases, 0, insert_id)
