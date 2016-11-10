import colander
import deform

from pyramid.view import view_config
from chameleon.template import BaseTemplateFile
from pymongo import MongoClient
import datetime
import pyramid.httpexceptions as exc

from pprint import pprint
from bson.objectid import ObjectId
import xlwt
import StringIO
from pyramid.response import FileResponse


from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )


from .security import USERS


@colander.deferred
def deferred_date_missing(node, kw):
   default_date = kw.get('default_date')
   if default_date is None:
       default_date = datetime.date.today()
   return default_date


css_widget = deform.widget.TextInputWidget(
    css_class='deformWidgetWithStyle')

class ArticleSearch(colander.Schema):
    eancode = colander.SchemaNode(
        colander.String(),
    widget = css_widget,
    )

class Article(colander.Schema):
    name = colander.SchemaNode(
            colander.String(),

            title=u"Artikelbezeichnung",
    )

    description = colander.SchemaNode(
        colander.String(),
        title=u"Beschreibung",
        missing=u"",
    )

    item_number = colander.SchemaNode(
            colander.String(),
            missing=unicode(''),
            title=u"Artikelnummer",
    )

    vendor = colander.SchemaNode(
        colander.String(),
        missing=unicode(''),
        title=u"Hersteller",
    )

    origin = colander.SchemaNode(
        colander.String(),
        missing=u"",
        title=u"Herkunft"
    )

    vendor_item_number = colander.SchemaNode(
            colander.String(),
            missing=unicode(''),
            title=u"Herstellerartikelnummer",
    )

    amount = colander.SchemaNode(
            colander.Integer(),
            title=u"Menge"
    )

    cost = colander.SchemaNode(
            colander.Float(),
            title=u"Einkaufspreis",
    )

    retail_price = colander.SchemaNode(
        colander.Float(),
        title=u"Verkaufspreis",
    )

    eancode = colander.SchemaNode(
        colander.String(),
        title = u"EAN-Code"
    )


class Stocktake(colander.Schema):
    inventory_stock = colander.SchemaNode(
            colander.Integer(),
    )

    stocktake_date = colander.SchemaNode(
            colander.Date(),
            title='Inventurdatum',
            default_date=datetime.date.today(),
            default = datetime.date.today(),






    )



@view_config(route_name='edit_article', renderer="templates/article_form.pt", permission='edit')
def edit_article(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['articles']
    collection = db['articles']
    schema = Article()
    editform = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = editform.validate(controls)
            appstruct['_id'] = ObjectId(request.matchdict['article_id'])
            appstruct['retail_prices'] = dict()
            appstruct['retail_prices']['common_brutto'] = appstruct['retail_price']


            collection.save(appstruct)
            raise exc.HTTPFound(request.route_url("articles"))


        except deform.ValidationFailure, e:
            return {'articleform': e.render(),
                    'values': False,
                    }

    article = collection.find_one({"_id": ObjectId(request.matchdict['article_id'])})
    article['retail_price'] = article['retail_prices']['common_brutto']
    return {'articleform': editform.render(appstruct=article)}

@view_config(route_name='search_article', renderer="templates/search_article.pt", permission='edit')
def search_article(request):
    schema = ArticleSearch()
    searchform = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = searchform.validate(controls)
            pprint(appstruct)
            client = MongoClient('mongodb://localhost:27017/')
            db = client['articles']
            collection = db['articles']
            article_data = collection.find_one({"eancode": appstruct['eancode']})
            pprint(article_data)
            try:
                article_data['_id']
            except:
                raise exc.HTTPFound(request.route_url("add_article"))
            raise exc.HTTPFound(request.route_url("stocktake_article", article_id=article_data['_id']))
        except deform.ValidationFailure, e:
            return {'articleform': e.render(),
                    'values': False,
                    }

    return {'articlesearchform': searchform.render()}



@view_config(route_name='add_article', renderer="templates/article_form.pt", permission='edit')
def add_article(request):
    schema = Article()
    addform = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = addform.validate(controls)
            pprint(appstruct)
            client = MongoClient('mongodb://localhost:27017/')
            db = client['articles']
            collection = db['articles']

            appstruct['retail_prices'] = dict()
            appstruct['retail_prices']['common_brutto'] = appstruct['retail_price']

            collection.insert_one(appstruct)
            raise exc.HTTPFound(request.route_url("articles"))



        except deform.ValidationFailure, e:
            return {'articleform': e.render(),
                    'values': False,
                    }

    return {'articleform': addform.render()}


@view_config(route_name='stocktake_article', renderer="templates/stocktake_form.pt", permission='edit')
def stocktake_article(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['articles']
    schema = Stocktake()
    addform = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = addform.validate(controls)
            pprint(appstruct)
            appstruct['stocktake_date'] = datetime.datetime.combine(appstruct['stocktake_date'],
                                                                    datetime.datetime.min.time())  # str(appstruct['invoice_date'])

            stocktake = appstruct
            stocktake['article_id'] = request.matchdict['article_id']

            collection = db['stocktakes']


            collection.insert_one(stocktake)

            db['articles'].update_one(
                    {"_id": ObjectId(request.matchdict['article_id'])},
                    {
                        "$set": {
                            "amount": appstruct['inventory_stock']
                        },

                        "$currentDate": {"lastModified": True},
                    },

            )
            raise exc.HTTPFound(request.route_url("search_article"))



        except deform.ValidationFailure, e:
            return {'articleform': e.render(),
                    'values': False,
                    }

    collection = db['articles']
    article_data = collection.find_one({"_id": ObjectId(request.matchdict['article_id'])})
    return {'stocktakeform': addform.render(), 'article_data': article_data}


@view_config(route_name='article', renderer='templates/article_template.pt', permission='edit')
def show_article(request):
    article_data = {}
    client = MongoClient('mongodb://localhost:27017/')
    db = client['articles']
    collection = db['articles']

    article_data = collection.find_one({"_id": ObjectId(request.matchdict['article_id'])})
    collection = db['core_data']

    article_data['core_data'] = collection.find_one({})

    return article_data


@view_config(route_name='articles_xls_export', permission='edit')
def list_articles(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['articles']
    collection = db['articles']
    w = xlwt.Workbook()
    ws = w.add_sheet('Artikelbestand')
    row = 0
    col = 0
    for elem in ['Artikelnummer', 'Artikelbezeichnung', 'Menge', 'Einkaufspreis', 'Herstellerartikelnummer', 'EAN-Code']:
        ws.write(row, col, elem)
        col += 1
    col = 0
    row += 1
    from pyramid.config import Configurator
    conf = Configurator()
    for article in collection.find():
        ws.write(row, 0, article['item_number'])
        ws.write(row, 1, article['name'])
        ws.write(row, 2, article['amount'])
        ws.write(row, 3, article['cost'])
        ws.write(row, 4, article['vendor_item_number'])
        ws.write(row, 5, article['eancode'])
        row += 1



    output = StringIO.StringIO()
    w.save('/tmp/o.xls')

    # print output.read()
    response = FileResponse(
        '/tmp/o.xls',
        request=request,
        content_type='application/vnd.ms-excel'
        )
    return response
