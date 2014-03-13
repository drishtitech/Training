from openerp.osv import fields,osv
from time import strftime

class idea_votes(osv.osv):
    _name="idea.votes"
    _columns={
     'comment':fields.text("Comment",size=64),
     'vote':fields.selection([('-1','Not Voted'),
           ('0','Very Bad'),
           ('25','Bad'),
           ('50','Normal'),
           ('75','Good'),
           ('100','Very Good')],'Vote'),
     'description':fields.text("Description"),
     'idea_id':fields.many2one("idea.idea","Idea"),
     'user_id':fields.many2one("res.users","User"),
    }
    
class idea_vote_category(osv.osv):
    _name="idea.vote.category"
    _inherits={'idea.votes':"vote_id"}
    _columns={
        'information':fields.text("Information",size=64),
        'vote_id':fields.many2one('idea.votes','Vote'),
        }
         
class idea_idea(osv.osv):
    _name="idea.idea"
    _description="Idea model"
    _inherit=['mail.thread','ir.needaction_mixin']
    
    def vote_count(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return {}
        res={}
        vote_obj=self.pool.get('idea.votes')
        for idea in self.browse(cr,uid,ids,context=context):
            #print idea     #prints list with browse record
            if idea:
                vote_id=vote_obj.search(cr,uid,[('idea_id','=',idea.id)])
                res[idea.id]=len(vote_id)
        return res                           

    _columns={
     'name':fields.char("Idea",size=128,required=True),
     'description':fields.text('Description'),
     'opened':fields.boolean('Opened',help='Is this idea opened'),
     'creation_datetime':fields.date('Creation date'),
     'open_datetime':fields.datetime('Open'),
     'close_datetime':fields.datetime('Close'),
     'reopen_datetime':fields.datetime('Reopen'),
     'state':fields.selection([('new','New'),('open','Opened'),('close','Accepted'),('cancel','Refused')],'State'),
     'creator_id':fields.many2one('res.users','Creator',required=True),
     'vote_id':fields.one2many('idea.votes','idea_id','Votes'),
     'requirement_ids':fields.many2many('idea.requirements','res_idea_requirements_rel','idea_id','requirement_id','Requirements'),
     'category_id':fields.many2one('idea.category','Category'),
     'parent_idea_category_id':fields.many2one('idea.category','Parent Category'),
     'nbr':fields.function(vote_count, method=True, string="Number of Votes",type="integer"),
     'count':fields.integer("Count"),
     'email':fields.related('creator_id',
                'user_email',
                type="char",
                string="Email",
                store=False),
    }
    _defaults={
              'state':'new',
              'nbr':1,
              'creation_datetime':strftime("%Y-%m-%d"),
             }
    _order='name desc'
    
    _sql_constraints=[
    ('name','unique(name,creator_id)','The Name and Creator of the Idea must be unique')]
   
    def _check_open_close_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,['open_datetime','close_datetime'],context=context):
   
            if idea['open_datetime'] and idea['close_datetime'] and idea['open_datetime'] > idea['close_datetime']:
                return False
            return True
   
    _constraints=[
            (_check_open_close_date,'Error! close date must be greater than opening date',['open_datetime','close_datetime'])]
    
    def on_change_category(self,cr,uid,ids,category_id,context=None):
        idea_category_obj=self.pool.get('idea.category').browse(cr,uid,category_id,context=context)
        #print idea_category_obj
        if category_id:    
            parent_idea_category_id=idea_category_obj.parent_id.id
        return {'value':{'parent_idea_category_id':parent_idea_category_id}}  
    
    def create(self,cr,uid,vals,context=None):
        if vals['description']==False:
            description1="This is default description"
            vals.update({'description':description1})
        print vals
        return super(idea_idea,self).create(cr,uid,vals,context=context)    
            

    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('open_datetime',False):
            vals.update({'opened':True})
        return super(idea_idea,self).write(cr,uid,ids,vals,context=context)  
    
    #WorkFlow_Activity Method
    
    def wkf_act_idea_opened(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'open','open_datetime':strftime('%Y-%m-%d %H:%M:%S'),'close_datetime':None})
        return True
    
    def wkf_act_idea_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'close','close_datetime':strftime('%Y-%m-%d %H:%M:%S'),'open_datetime':None})
        return True
         
class add_fields_in_idea_idea(osv.osv):
    _name="idea.idea"
    _inherit="idea.idea"
    _columns={
        'vote_limit':fields.integer('Maximum vote per user'),      
        }
    _defaults={
        'vote_limit':1,       
        }
    _sql_constraints=[('vote_limit_positive','check(vote_limit>0)','Maximum vote per user must be greater than zero')]    
    
   
class idea_requirements(osv.osv):
    _name='idea.requirements'
    _columns={ 
     'name':fields.char('Requirements',size=64,required=True),
     }
    
    
    
class idea_category(osv.osv):
    _name="idea.category"
    _columns={
              'name':fields.char('Category',size=64,required=True),
              'parent_id':fields.many2one('idea.category','Parent Category'),
              'child_ids':fields.one2many('idea.category','parent_id','Child Categories'),
               }
        
        