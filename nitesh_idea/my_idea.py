from openerp.osv import fields,osv
import time

class _idea_voters_category(osv.osv):
    _name='idea.voters.category'
   
    
    _columns={
              'information':fields.text('Information',size=64),
             }
    

class idea_voters(osv.osv):
    _name="idea.voters"
    _inherits={'idea.voters.category':'vote_id'}
    
    _columns={
             'comments':fields.text("Comments",size=110),
             'decision':fields.selection([('-1','Not voted'),('0','Very bad'),('1','Bad'),('2','Normal'),('3','Good'),('4','Very Good')],"Selection"),
             'posted_date':fields.date('Posted Date'),
             'user_id':fields.many2one('res.users','Voter'),
             'idea_id':fields.many2one('idea.idea','Idea'),
             'vote_id':fields.many2one('idea.voters.category','Vote', ondelete='cascade', required=True)
             }
    _defaults={
               'user_id':lambda self,cr,uid,context:uid,
               'decision':'-1',
               'posted_date':time.strftime('%Y-%m-%d %H:%M:%S')
               }
   


class idea_idea(osv.osv):
    _name="idea.idea"
    _description="Idea model"
    
    
    
    def _vote_count(self,cr,uid,ids,name,arg,context=None): #name=obj name to search,arg=list of tuples specifying search criteria
        if not ids:         #if no ids present then return empty {}
            return {}
        res={}
        idea_vote_obj=self.pool.get('idea.voters')  #make obj of idea.voters
        for idea in self.browse(cr,uid,ids,context=context):    #returns list of obj i.e ids of all ideas
            if idea:
                vote_ids=idea_vote_obj.search(cr,uid,[('idea_id','=',idea.id)])#returns list of ids of records matching the criteria
                res[idea.id]=len(vote_ids)
                
        return res
            
    
    _columns={
              'name':fields.char('Name'),
              'description':fields.text('Description'),
              'nbr':fields.integer('MAX. Votes per user'),
              'opened':fields.boolean('Opened ?',help='is this idea opened ?'),
              'creation_date': fields.date('Creation Date'),
              'opened_date':fields.datetime('Opened Date'), 
              'closed_date':fields.datetime('Closed Date'),
              'creator_id':fields.many2one('res.users','Creator'),
              'vote_ids':fields.one2many('idea.voters','idea_id','Vote'),
              'category_id':fields.many2one('idea.category','Category'),
              'requirement_ids':fields.many2many('idea.requirements',
                             'res_idea_requirements_rel',
                                                'idea_id',
                                                'requirement_id',
                                                'Requirements'),
              'state':fields.selection([('new','New'),('opened','Opened'),('accepted','Accepted'),('refused','Refused')],'State'),
              'parent_idea_category_id':fields.many2one('idea.category','Parent Category'),
              
              'count_votes':fields.function(_vote_count, method=True, string="Number of Votes", type="integer"),
              
              'email':fields.related('creator_id',
                                     'user_email',
                                     type="char",
                                     string='E-mail',
                                     store=False)

              }

    _defaults={
               'state':'new',
               'nbr':1,
               'creator_id':lambda self,cr,uid,context:uid,
               'creation_date':time.strftime('%Y-%m-%d')
               }
    
    _order='name desc'
    
    _sql_constraints=[
          ('constraint_name','unique(name,creator_id)','The idea summary & creator of the idea must be unique')]
    
    def _check_open_close_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,['opened_date','closed_date'],context=context):#returns list of ownership {} for each requested record i.e. returns open & close datetime for each record
            if idea['opened_date'] and idea['closed_date'] and idea['closed_date']<idea['opened_date']:
                return False
        return True    
    
    _constraints=[(_check_open_close_date,'Error: Closing date should be Greater than Opening date',['opened_date','closed_date'])]
    
    
    def on_change_category(self,cr,uid,ids,category_id,context=None):
        #self.pool.get() will create object of idea.category & browse returns the category_id for cuurent user
        #uid=cuurent user
        #category_id=id or list of ids of category
        idea_category_obj=self.pool.get('idea.category').browse(cr,uid,category_id,context=context)
        if category_id:
            parent_idea_category_id=idea_category_obj.parent_id.id  #take id of the parent of current category
        return {'value':{'parent_idea_category_id':parent_idea_category_id}}  #asssign parent_id  
    
    
    def create(self,cr,uid,vals,context=None):  #vals is dictionary i.e. field values for new record
        if (vals['description']==False):        #check description .if false,then update as given
            description1='This is default description'
            vals.update({'description':description1})
        return super(idea_idea,self).create(cr,uid,vals,context=context)    #returns id of new record created
    
    def write(self,cr,uid,ids,vals,context=None):#vals is {} of field values to update
        if vals.get('opened_date',False):   #if condition is true then update
            vals.update({'opened':True})
            print vals
        return super(idea_idea,self).write(cr,uid,ids,vals,context=context) #returns true
    
    
#workflow_methods
    #display opened datetime when idea is opened
    def wkf_act_idea_opened(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'opened','opened_date':time.strftime('%Y-%m-%d %H:%M:%S'),'closed_date':None,'opened':True})
        return True 
    
    #display closed datetime when idea is accepted
    def wkf_act_idea_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'accepted','closed_date':time.strftime('%Y-%m-%d %H:%M:%S'),'opened_date':None,'opened':False})
        return True
        
    def wkf_act_idea_refused(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'refused','closed_date':time.strftime('%Y-%m-%d %H:%M:%S'),'opened_date':None,'opened':False})
        return True
    
   
       
class add_fields_in_idea_idea(osv.osv):
    _name='idea.idea'
    _inherit='idea.idea'
    
    _columns={
              'vote_limit':fields.integer('MAX. votes per user')
              }
    
    _defaults={
               'vote_limit':1
               }
    
    _sql_constraints=[('vote_limit_positive','check(vote_limit>0)','Maximum votes per user should be greater than Zero.')]
    
    
    
class idea_category(osv.osv):
    _name='idea.category'
    _columns={
              'name':fields.char('Category'),
              'parent_id':fields.many2one('idea.category','Parent Category'),
                'child_ids':fields.one2many('idea.category','parent_id','Child Category')
              }
    
    
class idea_requirements(osv.osv):
    _name='idea.requirements'
    _columns={
              'name':fields.char('Requirement')}
    
    
    
    