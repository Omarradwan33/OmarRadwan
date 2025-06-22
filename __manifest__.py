{
    'name': "Hospital System",

    'author': "Elgawhara",
    'licence': 'LGPL-3',



    'version': '17.0.0.1.0',

    'category':'Healthcare',

    'depends': [
                'base' ,
                'mail',
                'product',
                ],


    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_views.xml',
        'views/department_views.xml' ,
        'views/doctors_views.xml' ,
        'views/menu.xml' ,
        'wizard\patient_transfer_wizard.xml',
        'reports\patient_report.xml',



    ],


   # 'images': ['static/description/icon.png'],
    'installable': True,
    'application': True



}
