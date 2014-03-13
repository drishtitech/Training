from osv import osv, fields
import time

class idea_vote_info(osv.osv):
    _name = "idea.vote.info"
    _columns = {
            'info': fields.text('Information'),
    }
    
class idea_vote(osv.osv):
    _name = "idea.vote"
    _inherits = {'idea.vote.info': "vote_info_id"}
    _columns = {
            'posted_date': fields.date('Posted Date'),
            'user_id': fields.many2one('idea.user','Voter'),
            'idea_id': fields.many2one('my.idea','Idea'),
            'comment': fields.text('Voter\'s Comment'),
            'decision': fields.selection([('-1','Not voted'),('0','Very Bad'),('25','Bad'),('50','Average'),('75','Good'),('100','Very Good')],'Vote'),
            'vote_info_id': fields.many2one('idea.vote.info', 'Vote ID', ondelete="cascade", required=True)
    }
    _defaults = {
            'decision':'-1',
            'posted_date': time.strftime('%Y-%m-%d'),
            'user_id': lambda self,cr,uid,context: uid,
    }  

    
class my_idea(osv.osv):
    _name = "my.idea"
    _inherit = ['mail.thread','ir.needaction_mixin']
    
    def vote_count(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return {}
        res = {}
        vote_obj = self.pool.get('idea.vote')
        for idea in self.browse(cr,uid,ids,context=context):
            if idea:
                vote_ids = vote_obj.search(cr,uid,[('idea_id','=',idea.id)])
                res[idea.id] = len(vote_ids)
        return res

    _columns = {
            'name': fields.char('Name', required=True),
            'description': fields.text('Description'),
            'creation_date': fields.date('Creation Date'),
            'creation_datetime': fields.datetime('Open'),
            'close_datetime': fields.datetime('Close'),
            'state': fields.selection([('new','New'),('open','Opened'),('close', 'Accepted'),('cancel', 'Rejected')],'State'),
            'creator_id': fields.many2one('idea.user','Creator', required=True),
            'vote_ids': fields.one2many('idea.vote','idea_id','Vote'),
            'requirement_ids': fields.many2many('idea.requirement', 'idea_requiremen_rel', 'idea_id', 'requirement_id', 'Requirements'),
            'category_id': fields.many2one('idea.category','Category'),
            'count': fields.function(vote_count, method=True, string="Number of votes", type="integer"),
            'parent_category_id': fields.many2one('idea.category', 'Parent category'),
            'email': fields.related('creator_id', 'user_email', type="char", string="Email of Creator", store=False),            
    }
    _defaults = {
            'state':'new',
            'creation_date': time.strftime('%Y-%m-%d'),
            #'creation_datetime': time.strftime('%Y-%m-%d %H:%M:%S'),
            'creator_id': lambda self,cr,uid,context: uid,
            'count': 0,
    }
    _order = 'name asc'
    
    _sql_constraints = [
            ('my_idea_unique','unique(name, creator_id)','Name of your idea and creator must be unique')]
    
    def my_idea_check_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,[],context=context):
            if idea['creation_datetime'] and idea['close_datetime'] and idea['creation_datetime'] > idea['close_datetime']:
                return False
            return True
    
    _constraints = [
            (my_idea_check_date,'Closing datetime is less than opening datetime',['creation_datetime','close_datetime'])]
    
    def on_change_category(self,cr,uid,ids,category_id,context=None):
        idea_category_obj = self.pool.get('idea.category').browse(cr,uid,category_id,context=context)
        if category_id:
            parent_category_id = idea_category_obj.parent_id.id
        return {'value':{'parent_category_id' : parent_category_id}}  
        
    def create(self,cr,uid,vals,context=None):
        if vals['description'] == False:
            default_description = 'You have not provided any description for your idea...'
            vals.update({'description' : default_description})
        return super(my_idea,self).create(cr,uid,vals,context=context)
    
    #def write(self,cr,uid,ids,vals,context=None):
        #if vals.get('creation_datetime',False):
            #vals.update({'opened' : True})
        #return super(my_idea, self).write(cr,uid,ids,vals,context=context)
    
    #Workflow's Activity Methods
    def my_idea_opened(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'open','creation_datetime': time.strftime('%Y-%m-%d %H:%M:%S'),'close_datetime':None,'opened':True})
        return True
    
    def my_idea_accepted(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'close','close_datetime':time.strftime('%Y-%m-%d %H:%M:%S'),'creation_datetime':None,'opened':False})
        return True
    
    def my_idea_rejected(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'cancel','close_datetime':time.strftime('%Y-%m-%d %H:%M:%S'),'creation_datetime':None,'opened':False})
        return True
    
class add_my_idea(osv.osv):
    _name = "my.idea"
    _inherit = 'my.idea'
    _columns = {
            'vote_limit':fields.integer('Votes per user'),
            'opened':fields.boolean('Opened')
    }
    _defaults = {
            'vote_limit':1
    }
    
class idea_user(osv.osv):
    _name = "idea.user"
    _columns = {
            'name': fields.char('User', required=True),
            'user_email':fields.char('Email')
    }
    
class idea_Requirement(osv.osv):
    _name = "idea.requirement"
    _columns = {
            'name': fields.char('Requirements', required = True)
    }
    
class idea_category(osv.osv):
    _name = "idea.category"
    _columns = {
            'name': fields.char('Category'),
            'parent_id':fields.many2one('idea.category', 'Parent Category'),
            'child_id': fields.one2many('idea.category', 'parent_id', 'Child Category')
    }
