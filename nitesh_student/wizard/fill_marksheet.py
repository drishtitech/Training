from openerp.osv import osv,fields

class student_fill_marksheet(osv.osv_memory):
    _name='student.fill.marksheet'
    
    _columns={
              'sem_number':fields.selection([('sem1','semester 1'),('sem2','semester 2'),('sem3','semester 3'),('sem4','semester 4')],'Semester',required=True),
              'mark_sub1':fields.integer('Maths',size=2),
              'mark_sub2':fields.integer('C++',size=2),
              'mark_sub3':fields.integer('Java',size=2)
             }
    
    def fill_marks(self,cr,uid,ids,context=None):
        marksheet_id=context and context.get('active_ids',[]) or []
        student_marksheet_obj=self.pool.get('student.marksheet')
        wiz_obj=self.browse(cr,uid,ids)[0]
        for student_id in marksheet_id:
            marks={
                   'student_id':student_id,
                   'sem_number':wiz_obj.sem_number,
                   'm_sub1':wiz_obj.mark_sub1,
                   'm_sub2':wiz_obj.mark_sub2,
                   'm_sub3':wiz_obj.mark_sub3
                   }
            
            marks=student_marksheet_obj.create(cr,uid,marks)
            
        return {'type':'ir.actions.act_window_close'}
                
        

