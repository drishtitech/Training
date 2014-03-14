{
    'name': 'Student Management',
    'version': '0.1',
    'category': 'Tools',
    'description': """
This module meant for creating and maintaining student records.
=======================================================================================

It allows everybody to express ideas about different subjects.
Then, other users can comment on these ideas and vote for particular ideas.
Each idea has a score based on the different votes.
The managers can obtain an easy view of best ideas from all the users.
Once installed, check the menu 'Ideas' in the 'Tools' main menu.""",
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
    'depends': ['mail'],
    'data': ['./wizard/post_marksheet_view.xml','student_student_view.xml'],
    'demo': [],
    'test':[],
    'installable': True,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
