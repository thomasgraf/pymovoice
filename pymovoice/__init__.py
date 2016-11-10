from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .security import groupfinder

from pyramid.security import (
    Allow,
    Everyone,
    )

class RootACL():
    __name__ = None
    __parent__ = None
    __acl__ = [
                (Allow, 'group:viewer', 'view'),
                (Allow, 'group:viewer', 'edit'), ]

    def __init__(self, request):
        pass



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()


    config = Configurator(settings=settings, root_factory=RootACL)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_chameleon')
    config.include('pyramid_fanstatic')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(name='/', path='./static/app')
    config.add_static_view('deform_static', 'deform:static')
    config.add_static_view('css', 'css', cache_max_age=1)
    config.add_route('external_article_search', '/api/v1/external_article/{eancode}.json')
    config.add_route('invoice', '/invoices/{invoice_id}/print')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('article', '/articles/{article_id}/print')
    config.add_route('add', '/add')
    config.add_route('add_invoice', '/invoices/add')
    config.add_route('edit_invoice', '/invoices/{invoice_id}/edit')
    config.add_route('add_article', '/articles/add')
    config.add_route('edit_article', '/articles/{article_id}/edit')
    config.add_route('stocktake_article', '/articles/{article_id}/stocktake')
    config.add_route('invoices', '/invoices/')
    config.add_route('articles', '/articles/')
    config.add_route('search_article', '/articles/eancode/search')
    config.add_route('articles_xls_export', '/articles/xls')
    config.scan()
    return config.make_wsgi_app()
