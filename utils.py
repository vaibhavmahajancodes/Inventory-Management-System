def check_low_stock(products):
    alerts = []
    for p in products:
        if p[2] <= p[4]:
            alerts.append({"id": p[0], "name": p[1], "quantity": p[2]})
    return alerts