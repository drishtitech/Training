from openerp.osv import osv,fields
import time

class idea_vote_category(osv.osv):
    _name='idea.vote.category'
    
    _columns={
                'information': fields.char('Information', size=64),
                
            }   
# This is a comment... Do not worry...
class idea_vote(osv.osv):
    _name='idea.vote'
    _inherits={'idea.vote.category': "vote_id"} 
    _columns={
              'decision': fields.selection([('notvoted','Not Voted'),('verybad','Very Bad'),('bad','Bad'),('normal','Normal'), ('good','Good'),('vgood','Very Good')]),
              'comment': fields.text('Comment'),
              'user_id': fields.many2one('res.users','Voter'),
              'idea_id': fields.many2one('idea.idea','Idea'),
              'posted_date': fields.datetime('Posted Date'),
              'vote_id': fields.many2one('idea.vote.category', 'Vote', ondelete='cascade', required=True)
              }
    _defaults={
               'decision':'good',     
               'posted_date': time.strftime('%Y-%m-%d %H:%M:%S'),
               
               }
    
 
    
class idea_idea(osv.osv):
    _name='idea.idea'
    
    #_inherit=['mail.thread', 'ir.needaction_mixin']
    
    def _vote_count(self,cr,uid,ids,name,arg,context=None):
            if not ids:
                    return {}
            res={}
            vote_obj=self.pool.get('idea.vote')#getting a sinlgeton instance of the class idea.vote
            
            for idea in self.browse(cr,uid,ids,context=context): # fetching each record idea on id from list 
                if idea:
                    vote_ids=vote_obj.search(cr,uid, [("idea_id", '=' ,idea.id)]) # for every matching idea_id inside idea.idea searching for idea_id inside idea.vote
                    res[idea.id]=len(vote_ids)
            return res
        
    _columns={
              'name': fields.char('Name',required=True),
              'description': fields.text('Description'),
              'creation_date': fields.date('Creation_Date'),
              'open_datetime':fields.datetime('Open'),
              'close_datetime':fields.datetime('Close'),
              'category_id': fields.many2one('idea.category','Category'),
              'count': fields.integer(string='Count'),
              'state': fields.selection([('new','New'),('open','Opened'),('close','Accepted'),('cancel','refused')],'State'),
              'user_id': fields.many2one('res.users','Creator',required=True),
              'voter_id': fields.one2many('idea.vote','idea_id','Voter_Id'),
              'requirement_id': fields.many2many('idea.requirements','res_idea_requirements_rel','idea_id','requirement_id','Requirements'),
              'is_open': fields.boolean('Is Open?'),
              'parent_idea_category_id':fields.many2one('idea.category','Parent Category'),
              'count_votes': fields.function(_vote_count, method=True, string="Number of Votes", type="integer"),
              'email': fields.related('user_id','user_email',type="char",string="Email",store=False)
              }
    _order='name desc'
    
    _sql_constraints = [('const_name','unique(name,user_id)','The Idea summary and creator of the idea must be unique')]
    
    def _check_open_close_date(self,cr,uid,ids,context=None):
            for idea in self.read(cr,uid,ids,['open_datetime','close_datetime'], context=context): # like select query fetching 2columns into dictionary idea !!check the whithout where cond n with ehrer cond
                    print idea;
                    if idea['open_datetime'] and idea['close_datetime'] and idea['open_datetime'] > idea['close_datetime'] :
                        return False
            return True
            
    _constraints=[(_check_open_close_date, 'Error! Idea close date time must be greater than open datetime',['open_datetime','close_datetime'])]
        
    def on_change_category(self, cr, uid, ids, category_id, context=None): #uid=singleton(user_id), ids=idea id, category_id=child id or selected id
        idea_category_obj=self.pool.get('idea.category').browse(cr, uid, category_id, context=context)# this will fetch browse_record(idea.category,category_id)
        if category_id:
            parent_idea_category_id=idea_category_obj.parent_id.id #this will fetch parent_id for the category selected 

        return {'value' : {'parent_idea_category_id' : parent_idea_category_id}}
        
    
    def create(self, cr, uid, vals, context=None):
        if vals['description']==False:
            description1='This is default description'
            vals.update({'description':description1})
        return super(idea_idea,self).create(cr,uid,vals,context=context)
    
    def write(self, cr, uid, ids,vals, context=None):
        if vals.get('open_datetime',False):
            vals.update({'is_open':True})
        return super(idea_idea,self).write(cr,uid,ids,vals,context=context)
    
    def wkf_act_idea_opened(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'open','open_datetime' : time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def wkf_act_idea_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'close','close_datetime' : time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
     
    _defaults={
               'state':'new',
               'user_id':lambda self,cr,uid,context:uid,
               'count': 1,
               'creation_date': time.strftime('%Y-%m-%d')
               
               }

class add_fields_in_idea_idea(osv.osv):
    _name='idea.idea'
    _inherit='idea.idea'
    _columns={
              'vote_limit': fields.integer('Maximum vote per user'),
              }
    _defaults={
               'vote_limit':1,
               }
    _sql_constraints=[('vote_limit_positive','check(vote_limit>0)','Maximum vote per user must be greater than zero')]

class idea_requirements(osv.osv):
    _name='idea.requirements'
    _columns={'name': fields.char('Requirement'),
              }
    
class idea_category(osv.osv):
    _name='idea.category'
    _columns={'name': fields.char('Category', size=64, required=True),
              'parent_id': fields.many2one('idea.category','Parent Category'),
              'child_ids': fields.one2many('idea.category','parent_id','Child Categories')
              }



    