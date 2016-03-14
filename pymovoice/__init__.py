from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_fanstatic')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_static_view('css', 'css', cache_max_age=1)
    config.add_route('invoice', '/invoices/{invoice_id}/print')
    config.add_route('add', '/add')
    config.add_route('add_invoice', '/invoices/add')
    config.add_route('edit_invoice', '/invoices/{invoice_id}/edit')
    config.add_route('invoices', '/invoices/')
    config.scan()
    return config.make_wsgi_app()
