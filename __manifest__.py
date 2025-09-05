{
    'name': 'Custom Debit Note Origin',
    'version': '17.0.1.0',
    'category': 'Accounting',
    'summary': 'Add origin invoice field for debit notes with client filter',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
}