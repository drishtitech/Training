from openerp.osv import fields,osv
from datetime import datetime
from datetime import date

class student_marksheet(osv.osv):
    _name="student.marksheet"
    _description="Student Marksheet"
    
    def total_count(self,cr,uid,ids,fields,arg,context):
        result={}
        for records in self.browse(cr,uid,ids):
            result[records.id]=records.physics + records.chemistry + records.maths
        return result  
    _columns={
        'name':fields.char("Marksheet"),
        'physics':fields.integer('Physics',size=64),
        'chemistry':fields.integer('Chemistry',size=64),
        'maths':fields.integer('Maths',size=64),
        'marksheet_id':fields.many2one('student.student','Student Marks'),  
        'Total':fields.function(total_count,method=True,string="Total Marks",type="integer"),    
        }

class student_student(osv.osv):
    _name="student.student"
    _description="Student Information"
    _columns={
        'name':fields.char("Student Name",size=128,required=True),
        'student_gender':fields.char("Gender",size=128,required=True),
        'addmission_date':fields.date("Addmission Date"),
        'student_name':fields.one2many("student.marksheet",'marksheet_id','Name of Student'),
        'student_birthdate':fields.date("DOB"),
        'age':fields.integer('Age'),
        'creator_id':fields.many2one('res.users','Creator',required=True),
        'physics':fields.integer('Physics',size=64),
        'chemistry':fields.integer('Chemistry',size=64),
        'maths':fields.integer('Maths',size=64),
       
        }
    
    def _addmission_birthdate_check_date(self,cr,uid,ids,context=None):
        for student in self.read(cr,uid,ids,['addmission_date','student_birthdate'],context=context):
            if student['addmission_date'] and student['student_birthdate'] and student['addmission_date'] < student['student_birthdate']:
                return False
            return True
    _constraints=[
            (_addmission_birthdate_check_date,'Invalid,your Date of Birth Must Be Greater Than Addmission Date',['addmission_date','student_birthdate'])]    

   
