
{
    'name': 'Student Information',
    'version': '1.0',
    'category': 'Tools',
    'description': """
Test
=================================================================

Student Management
""",
    'author': 'Drishti Tech',
    'website': 'http://student.com',
    'summary': 'Student Info',
    'sequence': 9,
    'depends':['mail'],
    'data': ['wizard/student_mark.xml','student_view.xml','student_workflow.xml'],
   
   
    'installable': True,
    'application': True,
    'auto_install': False,
}