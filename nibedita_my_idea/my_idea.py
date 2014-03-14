from osv import osv,fields
import time

class idea_vote_category(osv.osv):
    _name = "idea.vote.category"
    _columns={'information':fields.text('Information',size=64),
             # 'vote_id':fields.many2one('idea.vote','Vote',ondelete="cascade",required= True),
              }
    
class idea_vote(osv.osv):
    _name = 'idea.vote'
    _inherits={'idea.vote.category':"vote_id"}
    _columns={
              
        'user_id':fields.many2one('res.users','User'),
        'idea_id':fields.many2one('idea.idea','Idea'),
        'value':fields.selection([('-1','NO VOTE'),('5','VERYBAD'),('25','BAD'),('50','GOOD')],'selection'),
        'comment':fields.text('comment',size=64),
        'posteddate':fields.datetime('posteddate'),
        
        #'vote_id':fields.many2one('idea.vote','Vote',ondelete="cascade",invisible= True),

        }
class idea_idea(osv.osv):
    _name = 'idea.idea'
    
    
    
    def _vote_count(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return{}
        res={}
        vote_obj=self.pool.get('idea.vote')
        for idea in self.browse(cr,uid,ids,context=context):
            if idea:
                vote_id=vote_obj.search(cr,uid,[('idea_id','=',idea.id)])
                res[idea.id]=len(vote_id)
            return res 
        
    _columns={
        'name':fields.char('Ideasummery',size=64,required=True),
        'description':fields.text('description'),
        'nbr':fields.integer('nbr'),
        'opened':fields.boolean('open?', help='is this idea opened?'),
        'creator_id':fields.many2one('res.users','Creator', required=True),
        'vote_id':fields.one2many('idea.vote','idea_id','Vote'),
        'requirements_ids':fields.many2many('idea.requirments','res_idea_requirments_rel','idea_id','requirments_id','requirements'),
        'category_id':fields.many2one('idea.category','Category'),
        'state':fields.selection([('new','New'),('open','OPENED'),('close','Accepted'),('cancel','Refused')],'state'),
        'creation_date':fields.date('Date'),
        'create_datetime':fields.datetime('Date time'),
        'closing_date':fields.date('Date'),
        'parent_idea_category_id':fields.many2one('idea.category','Parent Category'),
        'email':fields.related('creator_id',
                               'user_email',
                               type="char",
                               string='Email',
                               store=False),
              
        'count_votes': fields.function(_vote_count,method=True,string="Number of Votes", type="integer"),
        }
    
    _defaults={
        'state':'new',
        'creator_id': lambda self,cr,uid,context:uid,
        'nbr':1,
        'creation_date': time.strftime('%Y-%m-%d'),
        }
    _order='name desc'
   
    _sql_constraints=[('name','unique(name,creator_id)','the Ideas Summary and creator of the Ideas must be unique!')] 
    
    def _check_open_close_date(self, cr, uid, ids, context=None):
        for idea in self.read(cr,uid,ids,['creation_date','closing_date'],context=None):
                if idea['creation_date'] and idea['closing_date'] and idea['creation_date']>idea['closing_date']:
                    return False
        return True
    
    _constraints=[(_check_open_close_date,'Error!Idea close date time must be greater the open date time.',['creation_date','closing_date'])] 
    
    def on_change_category(self,cr, uid,ids,category_id,context=None):
        idea_category_obj= self.pool.get('idea.category').browse(cr, uid, category_id, context=context)  
        if category_id:
            parent_idea_category_id=idea_category_obj.parent_id.id  
        return {'value':{'parent_idea_category_id': parent_idea_category_id}} 
    
    def create(self,cr,uid,vals,context=None):
        if vals['description']==False:
            description1 = 'This is default description'
            vals.update({'description': description1})
        return super(idea_idea,self).create(cr,uid,vals,context=context) 
    
    
    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('creation_date', False):
            vals.update({'opened':True})
        return super(idea_idea,self).write(cr,uid,ids,vals,context=context) 
   
    def wkf_act_idea_opened(self,cr,uid,ids): 
        self.write(cr,uid,ids,{'state':'open','creation_date':time.strftime('%Y-%m-%d')})
        return True
    
    def wkf_act_idea_accepted(self,cr,uid,ids): 
        self.write(cr,uid,ids,{'state':'close','closing_date':time.strftime('%Y-%m-%d')})
        return True
    
class add_fields_in_idea_idea(osv.osv):
    _name = 'idea.idea'
    _inherit="idea.idea"
    _columns={
              
        'vote_limit':fields.integer('Maximum Vote per User'),
        }
        
    _defaults = {
        
        'vote_limit':1,
        
         }   
    
    _sql_constraints=[('vote_limit_positive','check(vote_limit>0)','Maximum Vote per User must be greater than Zero')] 
    

class idea_requirements(osv.osv):
    _name = 'idea.requirments'
    _columns={
              'name':fields.char('Requirements',size=64,required=True),
  }
class idea_category(osv.osv):
    _name = 'idea.category'
    _columns={
        
        'name':fields.char('Category',size=64,required=True),
        'parent_id':fields.many2one('idea.category','Parent Category'),
                'child_ids':fields.one2many('idea.category','parent_id','Child Categories')
        
       }
    
   
    
    