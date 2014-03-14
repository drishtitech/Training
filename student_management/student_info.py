from osv import osv,fields
import time

class student_marksheet(osv.osv):
    _name='student.marksheet'
    
    def get_total(self, cr, uid, ids, fields, arg, context):
        x={}
        for record in self.browse(cr, uid, ids):
            x[record.id]= sum(record.english,record.marathi,record.science,record.java,record.c)
        return x
    
    _columns={
             
              'comment':fields.text('Comment',size = 64),
              
              'student_id':fields.many2one('student.info','Student'),
              'english':fields.integer('English'),
              'marathi':fields.integer('Marathi'),
              'science':fields.integer('Science'),
              'java':fields.integer('Java'),
              'c':fields.integer('C'),
              'total':fields.function(get_total, method=True, string='Total Mark',type='integer'),
              'semester':fields.selection([('semI','Semester I'),('semII','Semester II')],'Semester')
             }


class student_info(osv.osv):
    _name='student.info'
    
    
    
    _columns={
              'name':fields.char("Name"),
              'birth_date':fields.date('Date of Birth',required=True),
              'age':fields.integer("Age"),
              'admission_date':fields.datetime("Admission Date"),
              'semII_datetime':fields.datetime("SemII Admission"),
              'gender':fields.selection([('male','Male'),('female','Female')],'Gender'),
              'marksheet_id':fields.one2many('student.marksheet','student_id',"Mark sheet"),
              'description':fields.text("Description"),
              'address':fields.text("Address"),
              'semester':fields.selection([('semI','Semester I'),('semII','Semester II')],'Semester'),
              'state':fields.selection([('new','New'),('semI','SEM I'),('semII','SEM II'),('failed','Failed')],'SEMESTER'),
              'class':fields.char("Class")

              }
    
    def wkf_act_student_opened(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'semI','admission_date':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def wkf_act_student_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'semII','semII_datetime':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
   
    
#    def _check_open_close_date(self,cr,uid,ids,context=None):
#        for a in self.read(cr,uid,ids,['birth_date'],context=context):
#            if a['birth_date'] > a['admission_date'] and a[time.strftime('%Y-%m-%d %H:%M:%S')]:
#                return False
#        return True
#    _constraints=[(_check_open_close_date,'Error!Student Admission time must be greater then Birth date',['birth_date'])]
    
#    def onchange_getage_id(self,cr,uid,ids,birth_date,context=None):
#        current_date=datetime.now()
#        current_year=current_date.year
#        birth_year = parser.parse(birth_date)
#        current_age=current_year-birth_year.year
#        val = {'age':current_age}
#        return {'value': val}


