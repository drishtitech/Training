{
    'name': 'Student Information',
    'version': '1.0',
    'category': 'Tools',
    'description': """
This module is for maintaining  student information.
=======================================================

This module is the base module for  modules.
    """,
    'author': 'OpenERP SA,SYLEAM',
    'website': 'http://www.openerp.com/',
    'depends': ['base'],
    'data': ['wizard/sem_marks.xml','student_module1.xml','workflow.xml'],
    'installable': True,
    'auto_install': False,
}
