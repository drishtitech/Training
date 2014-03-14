from osv import fields,osv

# Creating separate wizard inside Student form for posting of Semester Subject Marks of Student
class student_post_marksheet(osv.osv_memory):
    _name="student.post.marksheet"
    _columns ={
        'sub1_mark': fields.float('English'),
        'sub2_mark': fields.float('Maths'),
        'sub3_mark': fields.float('Science'),
        'comment_mark': fields.text('Comments')
        }

# Function for posting marks in the student_marksheet table
    def post_marks(self,cr,uid,ids,context=None):
        student_ids=context and context.get('active_ids', []) or []
        mark_obj=self.pool.get('student.marksheet')
        wiz_obj=self.browse(cr,uid,ids)[0]
        for stud_id in student_ids:
            marksheet={'student_id':stud_id,
                       'name':uid,
                       'sub1': wiz_obj.sub1_mark,
                       'sub2': wiz_obj.sub2_mark,
                       'sub3': wiz_obj.sub3_mark,
                       'comment': wiz_obj.comment_mark
                       }
            marksheet=mark_obj.create(cr,uid,marksheet)
            return {'type':'ir.actions.act_window_close'}

# For Inserting marksheet at a later date for a particular student        
class student_select(osv.osv_memory):
    _name="student.select"
    _columns ={
        'student_id': fields.many2one('student.student', 'Student', required=True),
        }

# Function creating a new Form
    def separate_mark_form(self,cr,uid,ids,context=None):
        if context is None:
            context={}
        current_wiz_stud_id=self.browse(cr,uid,ids,context=context)[0].student_id.id
        data_obj=self.pool.get('ir.model.data')   
        database_id=data_obj._get_id(cr,uid,'nisha_stud_management','view_student_marks_post')
        if database_id:
            view_id=data_obj.browse(cr,uid,database_id,context=context).res_id
            value={'view_type':'form',
                  'view_mode':'form',
                  'res_model':'student.post.marksheet',
                  'views':[(view_id,'form'),(False,'tree'),(False,'calendar'),(False,'graph')],
                  'type':'ir.actions.act_window',
                  'target':'new',
                  'context':{'active_ids':[current_wiz_stud_id]}
                  }
            return value