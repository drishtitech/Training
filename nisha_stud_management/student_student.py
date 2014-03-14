from openerp.osv import osv
from openerp.osv import fields
import time
from datetime import date

# Creating Marksheets 
class student_marksheet(osv.osv):
    """ Students Marksheet """
    _name = "student.marksheet"
    _columns = {
        'name': fields.many2one('res.users', 'Student'),
        'marksheet_dt': fields.date('Marksheet Date'),
        'student_id': fields.many2one('student.student', 'Student Id',invisible=True),
        'sub1': fields.float('English'),
        'sub2': fields.float('Maths'),
        'sub3': fields.float('Science'),
        'comment': fields.text('Comments')
    }
    _defaults = {
        'marksheet_dt': lambda *a: time.strftime('%Y-%m-%d'),
        'name': lambda self, cr, uid, ctx: uid,
    }

# Creating Student main file
class student_student(osv.osv):
    """ Students """
    _name = "student.student"
    _inherit =['mail.thread', 'ir.needaction_mixin']
    
    _columns = {
        'name': fields.many2one('res.users', 'Student Name', required=True),
        'rollno': fields.integer('Roll No'),
        'gender': fields.selection([('male','Male'),('female','Female')], 'Gender'),
        'birth_date': fields.date('Birth-Date'),
        'admission_date': fields.date('Admission Date'),
        'remarks': fields.text('Remarks'),
        'age': fields.integer('Age'),
        'semester': fields.selection([('sem1','1st Semester'),('sem2', '2nd Semester'),('sem3','3rd Semester'),
                                      ('sem4','4th Semester')], 'Semester', track_visibility='onchange'),
        'stud_marks': fields.one2many('student.marksheet', 'student_id', 'Marksheet'),
       
    }
    _defaults = {
        'gender':'male',
        'birth_date': lambda *a: time.strftime('%Y-%m-%d'),
        'admission_date': lambda *a: time.strftime('%Y-%m-%d'),
        'semester': 'sem1'
    }
    
    _order = 'name asc'
   
    curr_today = date.today().strftime('%Y-%m-%d')
    print curr_today
    _sql_constraints=[('birthday_validator','check(birth_date > curr_today)','Please enter valid Birthdate !!')]
    
    def _check_birth_date(self,cr,uid,ids,context=None):
        for stud in self.read(cr,uid,ids,['birth_date','admission_date'],context=context):
            if stud['birth_date'] and stud['admission_date'] and stud['birth_date'] > stud['admission_date']:
                return False
        return True
    
    _constraints=[(_check_birth_date,'Birth date cannot be later than Admission Date',['birth_date','admission_date'])]
    
    def create(self,cr,uid,vals,context=None):
        if vals['age']==False:
            if vals['birth_date']==True:
                d0=vals.get('birth_date')
                delta=d0-curr_today
                age1=delta.days
                vals.update({'age':age1})
        return super(student_student, self).create(cr,uid,vals,context=context)