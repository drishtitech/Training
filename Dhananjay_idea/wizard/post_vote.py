from osv import osv,fields
class idea_post_vote(osv.osv_memory):
    _name="idea.post.vote"
    _description="Post Vote for Idea"
    _columns={
              'vote':fields.selection([('-1','Not voted'),
                                       ('0','very bad'),
                                       ('25','Bad'),
                                       ('50','normal'),
                                       ('75','good'),
                                       ('100','very good')],
                                       'Post Vote',required=True),
              'note':fields.text('Description')
              }
    def do_vote(self,cr,uid,ids,context=None):
        idea_ids=context and context.get('active_ids',[]) or []
        vote_obj=self.pool.get('idea.vote')
        wiz_obj=self.browse(cr,uid,ids)[0]
        for idea_id in idea_ids:
            vote={
                  'idea_id':idea_id,
                  'user_ids':uid,
                  'opened':wiz_obj.vote,
                  'comment':wiz_obj.note
                  }
            vote=vote_obj.create(cr,uid,vote)
            return{'type':'ir.actions.act_window_close'}

class idea_select(osv.osv_memory):
    _name = "idea.select"
    _description="Select Idea"
    _columns={
              'idea_id':fields.many2one('idea.idea','Idea',required =True)
              }
    def open_vote_form(self,cr,uid,ids,context=None):
        if context is None:
            context ={}
        current_wiz_idea_id=self.browse(cr,uid,ids,context=context)[0].idea_id.id
        data_obj=self.pool.get('ir.model.data')
        database_id=data_obj._get_id(cr,uid,'My_idea','view_idea_post_vote')
        if database_id:
            view_id=data_obj.browse(cr,uid,database_id,context=context).res_id
            value={
                    'view_type':'form',
                    'view_mode':'form',
                    'res_model':'idea.post.vote',
                    'views':[(view_id,'form'),(False,'tree'),(False,'calendar'),(False,'graph')],
                    'type':'ir.actions.act_window',
                    'target':'new',
                    'context':{'active_ids':[current_wiz_idea_id]}
                    }
            return value