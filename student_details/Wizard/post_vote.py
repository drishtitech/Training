from osv import fields,osv
class student_details_wiz(osv.osv_memory):
    _name ="student.details.wiz"
    _description="post vote for idea"
    _columns={
               'gender': fields.selection([('yes','YES'),('no','NO')],'post vote',required=True),
                'note':fields.text('Description')
                }
    
    def do_vote(self,cr,uid,ids,context=None):
        idea_ids=context and context.get('active_ids',[])or []
        vote_obj=self.pool.get('idea.vote')
        wiz_obj=self.browse(cr,uid,ids)[0]
        for idea_id in idea_ids:
            vote={
                  'idea_id':idea_id,
                  'user_id':uid,

            
