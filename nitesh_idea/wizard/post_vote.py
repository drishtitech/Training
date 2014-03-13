from openerp.osv import osv,fields

class idea_post_vote(osv.osv_memory):
    _name='idea.post.vote'
    _columns={
              'vote':fields.selection([('-1','Not voted'),('0','Very bad'),('1','Bad'),('2','Normal'),
                                       ('3','Good'),('4','Very good')], 'Post Vote', required=True),
              'note':fields.text('Comments'),
              'info':fields.text('Information')
              }
    
    def do_vote(self,cr,uid,ids,context=None):
        idea_ids=context and context.get('active_ids',[]) or []     #take active_ids which are currently active i.e. only one id active at a time
        vote_obj=self.pool.get('idea.voters')
        wiz_obj=self.browse(cr,uid,ids)[0]      #take ids of first record at 0th position
        for idea_id in idea_ids:
            vote={
                  'idea_id':idea_id,
                  'user_id':uid,
                  'decision':wiz_obj.vote,
                  'comments':wiz_obj.note,
                  'information':wiz_obj.info
                  }
            vote=vote_obj.create(cr,uid,vote)       #returns id of new record & creates new record in idea_voters table
        
        return {'type':'ir.actions.act_window_close'}   #for closing wizard after clicking on cancel button
        
        
class idea_select(osv.osv_memory):
    _name='idea.select'
    
    _columns={
              'idea_id':fields.many2one('idea.idea','Idea',required=True)
              }
    
    def open_vote_form(self,cr,uid,ids,context=None):
        if context is None:
            context={}
        current_wiz_idea_id=self.browse(cr,uid,ids,context=context)[0].idea_id.id  
        print 'CW IDEA ID',current_wiz_idea_id #taking idea id of first wizard
        data_obj=self.pool.get('ir.model.data')
        database_id=data_obj._get_id(cr,uid,'my_idea','view_idea_post_vote') 
        print 'DB ID',database_id       #taking id from ir_model_data table i.e .LHS column id  of ir_model_data
        if database_id:
            view_id=data_obj.browse(cr,uid,database_id,context=context).res_id      #taking id of form view i.e. integer
            print 'VIEW ID',view_id   #RHS column res_id in ir_model_data table
        value={
               'name':'Voting form',
               'view_type':'form',
               'view_mode':'form',
               'res_model':'idea.post.vote',
               'views':[(view_id,'form'),(False,'tree'),(False,'calendar'),(False,'graph')],
               'type':'ir.actions.act_window',
               'target':'new',
               'context':{'active_ids':[current_wiz_idea_id]}         #pass current idea selected in first wizard in context
               }
        
        return value
    
    
    
    
    
    
    
    
    
    
    