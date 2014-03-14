from osv import osv, fields
import time
class student_mark(osv.osv):
    _name="student.mark"
    _columns={
              'u_id':fields.many2one('student.details','UID'),
              'physics':fields.integer('Physics'),
              'Java': fields.integer('Java'),
              'C++':fields.integer('C++')
              }
class student_details(osv.osv):
    _name = "student.details"
    _inherit =['mail.thread', 'ir.needaction_mixin']
    _columns = {
            'name': fields.char('Name',required=True),
            'id': fields.integer('Student ID'),
            'gender': fields.selection([('male','Male'),('female','Female')],'Gender'),
            'birthday': fields.datetime('Birthday'),
            'age': fields.integer('Age'),
            'admission': fields.datetime('Admission'),
            'marksheet_id':fields.one2many('student.mark','u_id','Marksheet')
               }
    def my_check_open_close_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,['birthday','admission'], context=context):
            if  idea['birthday'] > idea['admission'] and idea[time.strftime('%Y-%m-%d %H:%M:%S')]:
                return False 
                return True       
    _constraints = [
        (my_check_open_close_date,'Error !Birth date is greater then admission date ',['birthday','admission'])]
