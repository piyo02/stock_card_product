{
    'name': 'Stock Card in Product',
    'author': 'technoindo.com',
    'category': 'hidden',
    'version': '10.0',
    'summary': 'Summary the addon.',
    'description': '''Description the addon'''
                   ,
    'depends': ['product', 'stock'],
    'data': [
        'views/stock_card_temp.xml',
        'views/stock_card_views.xml',
        'security/ir.model.access.csv'
    ],
    'images': [''],
    'auto_install': False,
    'installable': True,
    'application': False,
}
