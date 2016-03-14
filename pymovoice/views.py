from pyramid.view import view_config
from chameleon.template import BaseTemplateFile
from pymongo import MongoClient
import datetime




@view_config(route_name='invoices',  renderer='templates/invoices.pt')
def list_invoices(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['invoices']
    collection = db['invoices']
    return {'invoices':[invoice
            for invoice in collection.find()]}


@view_config(route_name='add')
def add(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['invoices']
    collection = db['invoices']
    invoice = {
        "address": "Frau\nJuergen Gericke\nSomewhere. 32\n79183 Waldkirch",
        "invoice_number": "RG-2015-0015",
        "invoice_date": datetime.datetime(2015,8,17),
        "customer_id": "AG-00010",
        "salutation": "Sehr geehrte Damen und Herren",
        "invoice_pre_text": "Dolor lorem ipsum",
        "amount": 5,
        "invoice_items": [
            {
                "description": "Service",
                "quantity": 1,
                "unitprice": 5.0,
                "price_of_position": 5.0
            }
        ]
    }



    return collection.insert_one(invoice)
