import colander
import deform

from pyramid.view import view_config
from chameleon.template import BaseTemplateFile
from pymongo import MongoClient
import datetime
import pyramid.httpexceptions as exc

from pprint import pprint
from bson.objectid import ObjectId


class InvoiceItem(colander.Schema):
    description = colander.SchemaNode(
        colander.String()

    )

    quantity = colander.SchemaNode(
        colander.Integer()
    )

    unitprice = colander.SchemaNode(
        colander.Float()
    )

    price_of_position = colander.SchemaNode(
        colander.Float()
    )


class InvoiceItems(colander.SequenceSchema):
    item = InvoiceItem()


class Invoice(colander.Schema):
    invoice_number = colander.SchemaNode(
        colander.String(),

        title="Rechnungsnummer",
    )

    invoice_date = colander.SchemaNode(
        colander.Date(),
        title='Rechnungsdatum'
    )

    address = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget()
    )

    customer_id = colander.SchemaNode(
        colander.String()

    )

    salutation = colander.SchemaNode(
        colander.String()
    )

    invoice_pre_text = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget()
    )

    amount = colander.SchemaNode(
        colander.Float()

    )

    invoice_items = InvoiceItems()


@view_config(route_name='edit_invoice', renderer="templates/invoice_form.pt")
def edit_invoice(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['invoices']
    collection = db['invoices']
    schema = Invoice()
    editform = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = editform.validate(controls)
            appstruct['_id'] = ObjectId(request.matchdict['invoice_id'])
            appstruct['invoice_date'] = datetime.datetime.combine(appstruct['invoice_date'],
                                                                  datetime.datetime.min.time())  # str(appstruct['invoice_date'])
            collection.save(appstruct)
            raise exc.HTTPFound(request.route_url("invoices"))


        except deform.ValidationFailure, e:
            return {'invoiceform': e.render(),
                    'values': False,
                    }

    invoice = collection.find_one({"_id": ObjectId(request.matchdict['invoice_id'])})
    return {'invoiceform': editform.render(appstruct=invoice)}


@view_config(route_name='add_invoice', renderer="templates/invoice_form.pt")
def add_invoice(request):
    schema = Invoice()
    addform = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = addform.validate(controls)
            pprint(appstruct)
            client = MongoClient('mongodb://localhost:27017/')
            db = client['invoices']
            collection = db['invoices']
            appstruct['invoice_date'] = datetime.datetime.combine(appstruct['invoice_date'],
                                                              datetime.datetime.min.time())

            collection.insert_one(appstruct)
            raise exc.HTTPFound(request.route_url("invoices"))



        except deform.ValidationFailure, e:
            return {'invoiceform': e.render(),
                    'values': False,
                    }

    return {'invoiceform': addform.render()}


@view_config(route_name='invoice', renderer='templates/invoice_template.pt')
def show_invoice(request):
    invoice_data = {}
    client = MongoClient('mongodb://localhost:27017/')
    db = client['invoices']
    collection = db['invoices']
    print collection.find_one({"_id": ObjectId(request.matchdict['invoice_id'])})
    invoice_data =  collection.find_one({"_id": ObjectId(request.matchdict['invoice_id'])})
    collection = db['core_data']
    invoice_data['core_data'] = collection.find_one({})
    return invoice_data
