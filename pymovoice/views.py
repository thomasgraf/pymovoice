from pyramid.view import view_config
from chameleon.template import BaseTemplateFile
from pymongo import MongoClient
import datetime

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )

import pyramid.httpexceptions as exc

from .security import USERS

@view_config(route_name='login',
             renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return exc.HTTPFound(location=came_from,
                             headers=headers)
        message = 'Failed login'

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return exc.HTTPFound(location=request.resource_url(request.context),
                     headers=headers)



@view_config(route_name='articles',  renderer='templates/articles.pt', permission='view')
def list_articles(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['articles']
    collection = db['articles']
    return {'articles':[article
            for article in collection.find()]}



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
