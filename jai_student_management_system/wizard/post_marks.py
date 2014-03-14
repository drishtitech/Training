from osv import fields,osv

class student_post_marks(osv.osv_memory):
    _name="student.post.marks"
    
    _description="Post marks for student"
    
    _columns={
        'sem_name': fields.selection([('sem1','SEM1'),('sem2','SEM2')],'Semester',required=True),
        'marks_java':fields.integer('Java'),
        'marks_sql':fields.integer('SQL'),
        'marks_c':fields.integer('C')
              }
                                       
    def do_post(self,cr,uid,ids,context=None):
        student_ids=context and context.get('active_ids',[]) or []
        marks_obj=self.pool.get('student.marksheet')
        #print 'vote_obj ',vote_obj
        wiz_obj=self.browse(cr,uid,ids)[0]
        #print 'wiz_obj ',wiz_obj
        
        for student_id in student_ids:
            marks={
                    'student_id': student_id,
                 #   'marksheet_id':marksheet_id,
                    'sem_name':wiz_obj.sem_name,
                    'marks_java':wiz_obj.marks_java,
                    'marks_sql':wiz_obj.marks_sql,
                    'marks_c':wiz_obj.marks_c
                  }
            marks=marks_obj.create(cr,uid,marks)
        return{'type': 'ir.actions.act_window_close'}
        
