import database_handler as handle

pro = []
op = []
cl = []
rt = []
pr = []
expn = []
expa = []
opd = []
cld = []
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
        handle.update("fuel", field, condition)
    except IndexError:
        insert_id = handle.select("count(*)", "fuel", "", "")[0][0]
        insert_id += 1
        handle.insert("fuel", insert_id, branch_id[0], str(sales_date[0]), pro[index],
                      op[index], cl[index], rt[index])
        real_insert(fuel_id, index, insert_id)
    return str(closing_stock - (opening_stock + rtt))


def sales_shs(index=0, litres=0, price=0):
    price = int(price)
    litres = float(litres)
    real_insert(pr, index, price)
    amount = litres * price
    real_insert(amount_array, index, amount)
    return str(amount), str(add_array(amount_array, index))


def expenses(index=0, exp_name="expense", exp_amount=0):
    exp_amount = int(exp_amount)
    real_insert(expn, index, exp_name)
    real_insert(expa, index, exp_amount)
    try:
        field = "name='" + expn[index] + "'," + "amount='" + str(expa[index]) + "'"
        condition = "id=" + str(expid[index])
        handle.update("expenses", field, condition)
    except IndexError:
        insert_id = handle.select("count(*)", "expenses", "", "")[0][0]
        insert_id += 1
        handle.insert("expenses", insert_id, branch_id[0], str(sales_date[0]),
                      expn[index], expa[index])
        real_insert(expid, index, insert_id)
    return str(add_array(expa, index))


def dips(index=0, opening_dips=0, closing_dips=0):
    opening_dips = float(opening_dips)
    closing_dips = float(closing_dips)
    real_insert(opd, index, opening_dips)
    real_insert(cld, index, closing_dips)
    try:
        field = "opening_dips='" + str(opd[index]) + "'," + "closing_dips='" + str(cld[index]) + "'"
        condition = "id=" + str(dips_id[index])
        handle.update("dips", field, condition)
    except IndexError:
        insert_id = handle.select("count(*)", "dips", "", "")[0][0]
        insert_id += 1
        handle.insert("dips", insert_id, branch_id[0], str(sales_date[0]),
                      opd[index], cld[index])
        real_insert(dips_id, index, insert_id)
    return str(opening_dips - closing_dips)


def lubricants(index=0, lub_name="lubricants", lub_amount=0):
    lub_amount = int(lub_amount)
    real_insert(lubn, index, lub_name)
    real_insert(luba, index, lub_amount)
    try:
        field = "name='" + lubn[index] + "'," + "amount='" + str(luba[index]) + "'"
        condition = "id=" + str(lubid[index])
        handle.update("lubricants", field, condition)
    except IndexError:
        insert_id = handle.select("count(*)", "lubricants", "", "")[0][0]
        insert_id += 1
        handle.insert("lubricants", insert_id, str(sales_date[0]), branch_id[0],
                      lubn[index], luba[index])
        real_insert(lubid, index, insert_id)
    return str(add_array(luba, index))


def prepaid(index=0, prepaid_name="prep", prepaid_amount=0):
    if len(prepaid_name) and len(prepaid_amount) > 0:
        prepaid_amount = int(prepaid_amount)
        real_insert(prepname, index, prepaid_name)
        real_insert(prepamount, index, prepaid_amount)
        try:
            field = "name='" + prepname[index] + "'," + "amount='" \
                    + str(prepamount[index]) + "'"
            condition = "id=" + str(prepaid_id[index])
            handle.update("prepaid", field, condition)
        except IndexError:
            insert_id = handle.select("count(*)", "prepaid", "", "")[0][0]
            insert_id += 1
            handle.insert("prepaid", insert_id, str(sales_date[0]), branch_id[0],
                          prepname[index], prepamount[index])
            real_insert(prepaid_id, index, insert_id)
        return str(add_array(prepamount, index))


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
        handle.update("debtors", field, condition)
    except IndexError:
        insert_id = handle.select("count(*)", "debtors", "", "")[0][0]
        insert_id += 1
        handle.insert("debtors", insert_id, str(sales_date[0]), branch_id[0], debtorn[index],
                      taken[index], paid[index])
        real_insert(debtor_id, index, insert_id)
    return add_array(paid, index), add_array(taken, index)


def login(user, password):
    users = " WHERE username=" + "'" + user + "' "
    passwords = "AND password='" + password + "'"
    result = handle.select(operation="id, username,pumps", table="users", condition1=users, condition2=passwords)
    if result:
        real_insert(branch_id, 0, result[0][0])
        return result[0][1], result[0][2]
    else:
        return 0


def cancel(table):
    handle.delete(table, sales_date[0])


def get_details():
    sales = get_data("fuel", fuel_id)
    mobile = get_data("mobile", mobile_id)
    prep = get_data("prepaid", prepaid_id)
    expense = get_data("expenses", expid)
    debtor = get_data("debtors", debtor_id)
    lubricant = get_data("lubricants", lubid)

    return sales, mobile, prep, expense, debtor, lubricant


def get_data(table, arr):
    result = handle.select("*", table, " WHERE branchid=" + str(branch_id[0]),
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
        handle.update("mobile", field, condition)
    except IndexError:
        insert_id = handle.select("count(*)", "mobile", "", "")[0][0]
        insert_id += 1
        handle.insert("mobile", insert_id, str(sales_date[0]), branch_id[0], airtels[index],
                      airtelw[index], mtns[index], mtnw[index])
        real_insert(mobile_id, index, insert_id)


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
