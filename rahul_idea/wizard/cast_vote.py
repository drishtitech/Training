from osv import osv,fields

class cast_vote(osv.osv_memory):
    _name="cast.vote"
    
    _description="Class defining fields for casting vote"
    
    _columns={
            'votes': fields.selection([('-1','Not voted'),('0','Very Bad'),('25','Bad'),('50','Average'),('75','Good'),('100','Very Good')],'Vote',required=True),
            'comment': fields.text('Your Comment'),
            'info' : fields.text('Information') 
    }
    
    def do_vote(self,cr,uid,ids,context=None):
        idea_ids = context and context.get('active_ids', []) or []
        vote_obj = self.pool.get("idea.vote")
        info_obj = self.pool.get("idea.vote.info")
        wiz_obj = self.browse(cr,uid,ids)[0]
        for i in idea_ids:
            vote = {'idea_id':i,'user_id':uid,'decision':wiz_obj.votes,'comment':wiz_obj.comment}
            vote = vote_obj.create(cr,uid,vote)
            info = {'info':wiz_obj.info}
            info = info_obj.create(cr,uid,info)
        return {'type':'ir.actions.act_window_close'}

class select_idea(osv.osv_memory):
    _name="select.idea"
    
    _description="Wizard for selecting the idea"
    
    _columns = {
            'idea_id': fields.many2one('my.idea', 'Select Idea', required=True)
    }
    
    def open_select_form(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        current_idea_id=self.browse(cr,uid,ids,context=context)[0].idea_id.id
        data_obj = self.pool.get('ir.model.data')
        db_id=data_obj._get_id(cr,uid,'my_idea','cast_vote_form_view')
        if db_id:
            view_id=data_obj.browse(cr,uid,db_id,context=context).res_id
            print 'View ID: ',view_id
            print 'DB ID: ',db_id
        value={
            'name':'Voting Form',
            'view_type':'form',
            'view_mode':'form',
            'res_model':'cast.vote',
            'view':[(view_id,'form'),(False,'tree'),(False,'calendar'),(False,'graph')],
            'type':'ir.actions.act_window',
            'target':'new',
            'context':{'active_ids':[current_idea_id]}}
        return value