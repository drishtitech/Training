from osv import osv,fields
import time

class student_marksheet_semester(osv.osv):
    _name = "student.marksheet.semester"
    _columns={
              
            'semester':fields.text('Semester'),
           
             
              }
    
class student_marksheet(osv.osv):
    _name = 'student.marksheet'
    _inherits={'student.marksheet.semester':"marksheet_id"}
    _columns={
              
        'user_id':fields.many2one('res.users','User'),
        'student_id':fields.many2one('student.student','student'),
        'result':fields.selection([('-1','FAIL'),('30','PASS'),('50','GOOD'),('70','VERYGOOD')],'GRADE'),
        'subject1':fields.integer('English'),
        'subject2':fields.integer('Maths'),
        'subject3':fields.integer('Science'),
        'subject4': fields.integer('History'),
        'issue_date':fields.date('date'),
        

        


        }
class student_student(osv.osv):
    _name = 'student.student'
    
    def _marks_count(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return{}
        res={}
        marks_obj=self.pool.get('student.marksheet')
        for student in self.browse(cr,uid,ids,context=context):
            if student:
                marksheet_id=marks_obj.search(cr,uid,[('student_id','=',student.id)])
                res[student.id]=len(marksheet_id)
            return res 




        
    _columns={
        'name':fields.char('Student Summery',size=64,required=True),
        'description':fields.text('description'),
        'age':fields.integer('Age'),
        'opened':fields.boolean('open?', help='is this idea opened?'),
        'creator_id':fields.many2one('res.users','Creator', required=True),
        'marksheet_id':fields.one2many('student.marksheet','student_id','Marks'),
        'requirements_ids':fields.many2many('student.requirments','res_student_requirments_rel','student_id','requirments_id','requirements'),
        'category_id':fields.many2one('student.category','Category'),
        'state':fields.selection([('new','New'),('open','OPEN'),('pass','PASS'),('next_semester','NEXT SEMESTER'),('fail','FAILED')],'state'),
        'creation_date':fields.date('Date'),
        'create_datetime':fields.datetime('Date time'),
        'birth_date':fields.date('Date'),
        'parent_student_category_id':fields.many2one('student.category','Parent Category'),
        'email':fields.related('creator_id',
                               'user_email',
                               type="char",
                               string='Email',
                               store=False),
        'count_marks': fields.function(_marks_count,method=True,string="total marks", type="integer"),
              
        
        }
    
    _defaults={
        'state':'new',
        'creator_id': lambda self,cr,uid,context:uid,
    
        'creation_date': time.strftime('%Y-%m-%d'),
        }
    _order='name desc'
   
    _sql_constraints=[('name','unique(name,creator_id)','the student Summary and creator of the student must be unique!')] 
    
    def _check_open_close_date(self, cr, uid, ids, context=None):
        for student in self.read(cr,uid,ids,['creation_date','birth_date'],context=None):
                if student['creation_date'] and student['birth_date'] and student['birth_date']>student['creation_date']:
                    return False
        return True
    
    _constraints=[(_check_open_close_date,'Error!Student birth date  must be greater the open date time.',['creation_date','birth_date'])] 
    

    def create(self,cr,uid,vals,context=None):
        if vals['description']==False:
            description1 = 'This is default description'
            vals.update({'description': description1})
        return super(student_student,self).create(cr,uid,vals,context=context) 
    
    
    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('creation_date', False):
            vals.update({'opened':True})
        return super(student_student,self).write(cr,uid,ids,vals,context=context) 
    
    
    
   
   
    def wkf_act_student_opened(self,cr,uid,ids): 
        self.write(cr,uid,ids,{'state':'open','creation_date':time.strftime('%Y-%m-%d')})
        return True
    
    def wkf_act_student_promoted(self,cr,uid,ids): 
        self.write(cr,uid,ids,{'state':'pass'})
        return True
   
  
    

class student_requirements(osv.osv):
    _name = 'student.requirments'
    _columns={
              'name':fields.char('Requirements',size=64,required=True),
  }
class student_category(osv.osv):
    _name = 'student.category'
    _columns={
        
        'name':fields.char('Category',size=64,required=True),
        'parent_id':fields.many2one('student.category','Parent Category'),
                'child_ids':fields.one2many('student.category','parent_id','Child Categories')
        
       }
    
   
    
    
