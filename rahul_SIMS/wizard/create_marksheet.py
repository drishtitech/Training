from osv import osv, fields

class create_marksheet(osv.osv_memory):
    _name="create.marksheet"
    
    _description="Class defining fields for creating marksheet"
    
    _columns={
        'semester' : fields.selection([('sem1','Semester 1'),('sem2','Semester 2'),('sem3','Semester 3'),('sem4','Semester 4')],'Semester'),
        'subject1' : fields.float('Score of Subject 1'),
        'subject2' : fields.float('Score of subject 2'),
        'subject3' : fields.float('Score of subject 3'),
    }
    
    def enter_marks(self,cr,uid,ids,context=None):
        student_ids = context and context.get('active_ids', []) or []
        marksheet_obj = self.pool.get("student.marksheet")
        wiz_obj = self.browse(cr,uid,ids)[0]
        for i in student_ids:
            marks = {'student_id':i,'semester':wiz_obj.semester,'subject1':wiz_obj.subject1,'subject2':wiz_obj.subject2,'subject3':wiz_obj.subject3}
            marks = marksheet_obj.create(cr,uid,marks)
        return {'type':'ir.actions.act_window_close'}
