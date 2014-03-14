from openerp.osv import fields,osv
from datetime import datetime
from time import strftime

class class_class(osv.osv):
    _name ="class.class"
    _columns={
        'class_name':fields.char("Class Name",size=64),
        'division_id':fields.many2one("division.division","Division"),
        'subject_id':fields.many2one("subject.subject","Subject Part"),
        'student_id':fields.many2one("student.student","Student"),
        'proffessor_id':fields.many2one("proffessor.proffessor","Proffessor"),
        'open_datetime':fields.datetime("Batch Start Date"),
        'close_datetime':fields.datetime('Batch End Date'),
        'parent_subject_subject_id':fields.many2one("subject.subject",'Main Subject'),
            }
    def on_change_subject(self,cr,uid,ids,subject_id,context=None):
        class_subject_obj=self.pool.get("subject.subject").browse(cr,uid,subject_id,context=context)
        if subject_id:
            parent_subject_subject_id=class_subject_obj.mainsubject_id.id
        return{'value':{'parent_subject_subject_id':parent_subject_subject_id}}                 
            
class division_division(osv.osv):
    _name="division.division"
    _columns={
        'name':fields.char("Class Division",size=64,required=True),
        'division':fields.one2many("class.class","division_id","Division Name"), 
          
              }
class subject_subject(osv.osv):
    _name="subject.subject"
    _columns={
        'subject':fields.one2many('class.class','subject_id'),
        'name':fields.char('Subject Part',size=64),
        'mainsubject_id':fields.many2one("subject.subject","Main Subject"),
        "part_id":fields.one2many("subject.subject","mainsubject_id"),
        }

class student_student(osv.osv):
    _name="student.student"
    _columns={
        'name':fields.char("Student Name",size=64),        
        'student_address':fields.char("Student Address",size=64),
        'student':fields.one2many('class.class','student_id','Student Name'),
        'subject':fields.char('Student Subject',size=64), 
              
              } 
       
class proffessor_proffessor(osv.osv):
    _name="proffessor.proffessor"
    _columns={
        'proffessor':fields.one2many('class.class','proffessor_id'),
        'subject_proffessor':fields.char('Proffesor Subject',size=64),
        'name':fields.char('Proffessor Name',size=64),
                  }
    