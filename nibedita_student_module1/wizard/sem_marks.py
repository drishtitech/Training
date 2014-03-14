from osv import fields,osv

class sem_marks(osv.osv_memory):
    _name="student.sem.marks"
    _description="marks for semesters"
    _columns={
          'marks':fields.selection([('-1','FAIL'),
                                    ('30','PASS'),
                                    ('50','GOOD'),
                                    ('70','VERYGOOD')
                                    ],
                                   
            'enter_marks',required=True),
            'note':fields.text('Description'),
              
              
     }
    
    def submit_marks(self,cr,uid,ids,context=None):
        student_ids = context and context.get('active_ids',[]) or []
        student_obj=self.pool.get("student.marksheet")
        wiz_obj =self.browse(cr,uid,ids)[0]
        for student_id in student_ids:
            marks={
                  'student_id':student_id,
                  'user_id':uid,
                  'value'  :wiz_obj.marks,
                  'comment':wiz_obj.note
              }
            marks=student_obj.create(cr,uid,marks)
        return{'type':'ir.actions.act_window_close'}
        
class student_select(osv.osv_memory):
    
    _name="student.select"
    _description="select students"
    _columns={'student_id':fields.many2one('student.student','student',required=True)
              }
    def open_marks_form(self,cr,uid,ids,context=None):
        if context is None:
            context={}
        current_wiz_student_id=self.browse(cr,uid,ids,context=context)[0].student_id.id
        data_obj=self.pool.get('ir.model.data')
        database_id=data_obj._get_id(cr,uid,'student_module','view_sem_marks')
        if database_id:
            view_id=data_obj.browse(cr,uid,database_id,context=context).res_id
            value={'view_type':'form',
                   'view_model':'form',
                   'res_model':'student.sem.marks',
                   'views':[(view_id,'form'),(False,'tree'),
                            (False,'calendar'),
                            (False,'graph')],
                   'type':'ir.actions.act_window',
                   'target':'new',
                   'context':{'active_ids':[current_wiz_student_id]}
                   }
            return value
                   
            
    
    
        
