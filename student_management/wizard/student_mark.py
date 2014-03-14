from osv import osv,fields
class post_marksheet(osv.osv_memory):
    _name="post.marksheet"
    _description="Make a Marksheet"
    _columns={
              'sem':fields.selection([('semI','Semester I'),
                                           ('semII','Semester II')],'Semester',required=True),
              'note':fields.text('Description')
              }
    def do_mark(self,cr,uid,ids,context=None):
        student_ids=context and context.get('active_ids',[]) or []
        mark_obj=self.pool.get('student.marksheet')
        wiz_obj=self.browse(cr,uid,ids)[0]
        for student_id in student_ids:
            sem={
                  'student_id':student_id,
               
                  'semester':wiz_obj.sem,
                  'comment':wiz_obj.note
                  }
            sem=mark_obj.create(cr,uid,sem)
            return{'type':'ir.actions.act_window_close'}
