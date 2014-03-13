from osv import osv, fields
import time

class idea_vote(osv.osv):
    _name='idea.vote'
    
    _columns={
              'opened':fields.selection([('-1','Not voted'),('0','very bad'),('25','Bad'),('50','normal'),('75','good'),('100','very good')],'Value'),
              'comment':fields.text('Comment',size = 64),
              'posted_date':fields.datetime('Posted Date'),     
              'user_id':fields.many2one('res.users','User'),
              'idea_id':fields.many2one('idea.idea','Idea'),
              }
    _defaults={
              'user_id': lambda self,cr,uid,context:uid,
              'opened':'-1',
              'posted_date': time.strftime('%Y-%m-%d %H:%M:%S'),
              }
    
class idea_vote_category(osv.osv):
    _name='idea.vote.category'
    _inherits={'idea.vote':"vote_id"}
    _columns={
              'information':fields.text('Information'),
              'vote_id':fields.many2one('idea.vote','Vote'),
              }   

class idea_idea(osv.osv):
    _name='idea.idea'
    _inherit=['mail.thread','ir.needaction_mixin']
    
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
              'name':fields.char('Idea Summary',size=64,required =True),
              'description':fields.text('Description'),
              'is_open':fields.boolean('Is Open'),
              'creation_date':fields.date('Creation Date'),
              'open_datetime':fields.datetime('Opening Date'),
              'close_datetime':fields.datetime('Closing Date'),
              'state':fields.selection([('new','New'),('open','Opened'),('close','Accepted'),('cancel','Refused')],'State'),
              'creator_id':fields.many2one('res.users','Creator'),
              'vote_id':fields.one2many('idea.vote','idea_id',"vote"),
              'requirement_id':fields.many2many('idea.requirements','idea_req_idea_rel','idea_id','requirement_id','Requirement'),
              'category_id':fields.many2one('idea.category','Category'),
              'count_vote':fields.function(_vote_count,methods =True,type='integer'),
              'count':fields.integer('Count'),
              'parent_idea_category_id':fields.many2one('idea.category','Parent Category'),
              'email': fields.related('creator_id','user_email',type="char",string="email",store=False)
              
              
              }
    _defaults={
              'state':'new',
              'creator_id': lambda self,cr,uid,context:uid,
              'count':1,
              'creation_date': time.strftime('%Y-%m-%d'),
              }
    _order='name'
    
    _sql_constraints=[('conatraint_name','unique(name,creator_id)','The Idea summary and creator of the idea must be unique!')]
    
    def _check_open_close_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,['open_datetime','close_datetime'],context=context):
            if idea['open_datetime'] and idea['close_datetime'] and idea['open_datetime'] > idea['close_datetime']:
                return False
        return True
    _constraints=[(_check_open_close_date,'Error!Idea close time must be greater then open date',['open_datetime','close_datetime'])]
    
    def on_change_category(self,cr,uid,ids,category_id,context=None):
        idea_category_obj=self.pool.get('idea.category').browse(cr,uid,category_id,context=context)
        if category_id:
            parent_idea_category_id=idea_category_obj.parent_id.id
        return {'value':{'parent_idea_category_id':parent_idea_category_id}}

    
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
        self.write(cr,uid,ids,{'state':'open','open_datetime':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def wkf_act_idea_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'close','close_datetime':time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    
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
    _columns={
              'name':fields.char('Requirement',size=64,required=True),
              }
    
class idea_category(osv.osv):
    _name='idea.category'
    _columns={
       'name':fields.char('category',size=64,required=True),  
       'parent_id':fields.many2one('idea.category','Parent Category'),
       'child_ids':fields.one2many('idea.category','parent_id','Child Category'),  
       }

        