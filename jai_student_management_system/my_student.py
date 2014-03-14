from openerp.osv import osv,fields

class student_student(osv.osv):
    _name='student.student'
    
    _columns={
                
                'name':             fields.char('Student_Name', required=True, size=64),
                'gender':           fields.selection([('male','Male'),('female','Female')],'Gender'),
                'birth_date':       fields.date('Date of Birth'),
                'age':              fields.integer('Age'),
                'admission_date':   fields.date('Date of Admission'),
                'marksheet_id':     fields.one2many('student.marksheet','student_id'),
                'state':            fields.selection([('unappeared','Unappeared'),('sem1','Sem1'),('sem2','Sem2'),('fail','Failed')],'State'),
                            
              
              }
    
    
class student_marksheet(osv.osv):
    _name='student.marksheet'
    

    _columns={
                
                'sem_name':         fields.selection([('sem1','SEM1'),('sem2','SEM2')],'Semester'),
                'marks_java':       fields.integer('Java'),
                'marks_sql':        fields.integer('SQL'),
                'marks_c':          fields.integer('C'),
                'marks_total':      fields.integer('Total Marks'),
                #'marks_total':      fields.function(_total_marks, method=True, string="Total Marks", type="integer"),
                'student_id':       fields.many2one('student.student','student')
              }
    

            