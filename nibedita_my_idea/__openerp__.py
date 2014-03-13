{
    'name': 'Idea Management',
    'version': '1.0',
    'category': 'Tools',
    'description': """
This module is for creating new a  ideas.
=======================================================

This module is the base module for  modules.
    """,
    'author': 'OpenERP SA,SYLEAM',
    'website': 'http://www.openerp.com/',
    'depends': ['base'],
    'data': ['wizard/post_vote_view.xml','my_idea_view.xml','workflow.xml','idea_report.xml'],
    'installable': True,
    'auto_install': False,
}