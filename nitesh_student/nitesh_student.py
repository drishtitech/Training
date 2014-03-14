from openerp.osv import osv,fields
from datetime import datetime
from dateutil import parser


class student_student(osv.osv): #main class ,maintains the student information
    _name='student.student'            
    
    _columns={
              'name':fields.char('Student name', size=50, required=True),
              'gender':fields.selection([('M','Male'),('F','Female')],'Gender'),
              'age':fields.char('Age'),
              'birth_date':fields.date('Birth date'),
              'admission_date':fields.date('Admission_date'),
              'marksheet_id':fields.one2many('student.marksheet','student_id','Semester'),   #foreign key with student.marksheet
              'state':fields.selection([('sem1','semester 1'),('sem2','semester 2'),('sem3','semester 3'),('sem4','semester 4')],'Semester')
              }
 
    
    _order='name' 
    
    _defaults={
              'state':'sem1'
              }
    
    
    def check_birth_date(self,cr,uid,ids,context=None):  #checks for birth_date should be less than today
        for student in self.read(cr,uid,ids,['birth_date'],context=context): #returns list of dictionaries for requested record i.e. for birth_date
            if student['birth_date'] and student['birth_date'] >= fields.date.today() : #check,if birth_date is present.if yes,then it should be less than today 
                return False    #means constraints is violated,display error msg
        return True
        
    def check_admission_date(self,cr,uid,ids,context=None):  #check for admission_date should be greater than birth_date
        for student in self.read(cr,uid,ids,['admission_date','birth_date'],context=None): #returns list of dictionaries for requested record i.e. for admission_date & birth_date of particular students 
            if student['admission_date'] and student['birth_date'] and student['admission_date']<= student['birth_date'] :
                return False    #means constraints is violated,display error msg
        return True 
    
    #constraints for birth_date < today ,admission_date > birth_date
    _constraints=[(check_birth_date,'Error : Birth date should be less than today',['birth_date']),
                  (check_admission_date,'Error: Admission date should be greater than birth date',['admission_date','birth_date'])]
    
   
    def on_change_birth_date(self,cr,uid,ids,birth_date,context=None):# to count age from birth date
        current_date= datetime.now()
        current_yr=current_date.year
        dob=parser.parse(birth_date)
        age_count=current_yr - dob.year
        val={'age':age_count}
        return {'value':val}
   
   
    def wkf_act_sem2(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'sem2'})
        return True 
    
    #display closed datetime when idea is accepted
    def wkf_act_sem3(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'sem3'})
        return True
        
    def wkf_act_sem4(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'sem4'})
        return True
    
   
   
   
    
class stduent_marksheet(osv.osv):   #class which maintains the marksheet records for different students
    _name='student.marksheet'
            
    def total_marks_count(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return {}
         
        res={}
        for student in self.browse(cr,uid,ids,context=context):
            if student:
                result=student.m_sub1 + student.m_sub2 + student.m_sub3
                res[student.id]=result
        return res
    
    
      
    
    _columns={
              'sem_number':fields.selection([('sem1','semester 1'),('sem2','semester 2'),('sem3','semester 3'),('sem4','semester 4')],'Semester'),
              'm_sub1':fields.integer('Maths',size=2),
              'm_sub2':fields.integer('C++',size=2),
              'm_sub3':fields.integer('Java',size=2),
              'student_id':fields.many2one('student.student','Student'), #foreign key with student.student
              'count_total':fields.function(total_marks_count, method= True, type='integer' ,string='Total marks')

           
              }