from osv import osv, fields
import time

class idea_vote_info(osv.osv):
    _name = "idea.vote.info"
    _columns = {
                'info':fields.text('information',size=64)
                }
    
class idea_vote(osv.osv):
    _name = "idea.vote"
    _inherits= {'idea.vote.info':"vote_info_id"}
    _columns = {
            'posted_date': fields.date('Posted Date'),
            'user_id': fields.many2one('res.users','Voter'),
            'idea_id': fields.many2one('my.idea','Idea'),
            'comment': fields.text('Your comment'),
            'decision': fields.selection([('yes','YES'),('no','NO')],'Select'),
            'vote_info_id': fields.many2one('idea.vote.info','vote info',ondelete='cascade',invisible=True) 
                }
    _defaults={
               'user_id':lambda self,cr,uid,context:uid,
               'decision':'no',
               'posted_date':time.strftime('%Y-%m-%d %H:%M:%S')
               }

class my_idea(osv.osv):
    _name = "my.idea"
    _inherit =['mail.thread', 'ir.needaction_mixin']
    def _vote_count(self, cr, uid, ids, name, arg, context=None):
            if not ids:
                    return{}
            res={}
            vote_obj = self.pool.get('idea.vote')
            for idea in self.browse(cr, uid, ids, context=context):
                if idea:
                    vote_ids=vote_obj.search(cr, uid, [('idea_id', '=' ,idea.id)])   
                    res[idea.id]=len(vote_ids) 
            return res
    _columns = {
            'name': fields.char('Name',required=True),
            'description': fields.text('Description'),
            'creation_date': fields.date('Creation Date'),
            'creation_datetime': fields.datetime('Open'),
            'close_datetime': fields.datetime('Close'),
            'state': fields.selection([('new','New'),('open','Opened'),('close', 'Accepted'),('cancel', 'Refused')],'State'),
            'creator_id': fields.many2one('res.users','Creator',required=True),
            'vote_ids': fields.one2many('idea.vote','idea_id','Vote'),
            'requirement_ids': fields.many2many('idea.requirement', 'idea_requiremen_rel', 'idea_id', 'requirement_id', 'Requirements'),
            'category_id': fields.many2one('idea.category','Category'),
            'count': fields.function(_vote_count,method=True,string="Number of votes",type="integer"),
            'parent_category_id': fields.many2one('idea.category','parent_category'), 
            'email': fields.related('creator_id','user_email', type="char", string="email", store=False),
            'opened': fields.boolean('opened')
    }
    _defaults={
             
             #'creation_datetime':time.strftime('%Y-%m-%d %H:%M:%S'),
              'state': 'new'
              }
    _order = 'name desc'
    _sql_constraints=[
                      ('name','unique(name,creator_id)','The idea summary and creator of the idea must be unique')]
    def my_check_open_close_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,['creation_datetime','close_datetime'], context=context):
            if idea['creation_datetime'] and idea['close_datetime'] and idea['creation_datetime'] > idea['close_datetime']:
                return False 
        return True
        
    _constraints = [
        (my_check_open_close_date,'Error !Idea close date time must be greater then open date time ',['creation_datetime','close_datetime'])]

    def on_change_category(self,cr,uid,ids,category_id,context=None):
        idea_category_obj=self.pool.get('idea.category').browse(cr,uid,category_id,context=context)
        if category_id:
            parent_category_id=idea_category_obj.parent_id.id
            
        return {'value':{'parent_category_id' : parent_category_id}}
    def create(self,cr,uid,vals,context=None):
        if vals['description']==False:
            default_description= "you have not provide the description for ur idea"
            vals.update({'description':default_description})
        return super(my_idea,self).create(cr,uid,vals,context=context)
    
    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('creation_datetime',False):
            vals.update({'opened':True})
     
        return super(my_idea,self).write(cr,uid,ids,vals,context=context)
    def wkf_act_idea_opened(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'open','creation_datetime':time.strftime('%Y-%m-%d %H:%M:%S'),'close_datetime':None})
        return True
    
    def wkf_act_idea_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'close','close_datetime':time.strftime('%Y-%m-%d %H:%M:%S'),'creation_datetime':None})
        return True
  
        
    
class add_my_idea(osv.osv):
    _name = "my.idea"
    _inherit = 'my.idea'
    _columns = {
            'vote_limit':fields.integer('Votes per user',size = 70)
    }
    _defaults = {
            'vote_limit':1
    }
class idea_Requirement(osv.osv):
    _name = "idea.requirement"
    _columns = { 
            'requirement': fields.char('Requirements', required = True)
    }
    
class idea_category(osv.osv):
    _name = "idea.category"
    _columns = {
            'name': fields.char('Category'),
            'parent_id':fields.many2one('idea.category', 'Parent Category'),
            'child_id': fields.one2many('idea.category', 'parent_id', 'Child Category')
            }
    