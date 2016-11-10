
from pyramid.view import view_config

from get_ean import get_ean

articles = {'4006260003252': 'Boss Stabilo Marker',
            '4311501436028' : 'EDEKA Bio Mozarella'}

@view_config(route_name='external_article_search', renderer='json')
def get_external_article(request):
  eancode = request.matchdict.get('eancode').strip()
  print eancode
  article = get_ean(eancode)
  #article = {'eancode': eancode, 'name': articles[eancode]}
  article['stockquantity'] = 0
  article['eancode'] = eancode
  print article
  return article

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyventur_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

