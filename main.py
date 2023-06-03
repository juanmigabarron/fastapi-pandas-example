from decimal import Decimal

import pandas
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/payments/")
def payments(paid: bool = None, currency: str = None):
    df = pandas.read_csv('data/payments.csv')
    if paid:
        df = df[df.paid == paid]
    if currency:
        df = df[df.currency == currency]
    payments_data = df.to_dict(orient='records')
    return {'data': payments_data}


@app.get("/payments/{payment_guid}")
def payment(payment_guid: str):
    df = pandas.read_csv('data/payments.csv')
    try:
        df = df[df.guid == payment_guid]
        payment_data = df.to_dict(orient='records')[0]
    except IndexError:
        payment_data = {}
    return {'data': payment_data}


@app.get("/balances/")
def balances():
    df = pandas.read_csv('data/payments.csv')
    payments_data = df.to_dict(orient='records')
    balances_data = {}
    for payment_data in payments_data:
        currency = payment_data['currency']
        amount = Decimal(payment_data['amount'])
        if currency in balances_data.keys():
            balances_data[currency] += amount
        else:
            balances_data[currency] = amount
    return {'data': balances_data}
