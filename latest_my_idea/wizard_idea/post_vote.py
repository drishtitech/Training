from osv import fields,osv

class idea_post_vote(osv.osv_memory):
    """Post Vote For Idea"""
    _name="idea.post.vote"
    _description="Post Vote For Idea"
    _columns={
         'vote':fields.selection([('-1','Not Voted'),
           ('0','Very Bad'),
           ('25','Bad'),
           ('50','Normal'),
           ('75','Good'),
           ('100','Very Good')],
         'Post Vote',required=True),
          'note':fields.text('Description'),    
              }
    
    def do_vote(self,cr,uid,ids,context=None):
        idea_ids=context and context.get('active_ids',[]) or []
        vote_obj=self.pool.get('idea.votes')
        wiz_obj=self.browse(cr,uid,ids)[0]
        for idea_id in idea_ids:
            vote={
              'idea_id':idea_id,
              'user_id':uid,
              'vote':wiz_obj.vote,
              'comment':wiz_obj.note,
              }
            vote=vote_obj.create(cr,uid,vote)
            return{'type':'ir.actions.act_window_close'}
            
 
            
                