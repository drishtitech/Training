from openerp.osv import osv
from openerp.osv import fields
import time

class idea_vote_category(osv.osv):
    _name="idea.vote.category"
   
    _columns ={
        'information': fields.text('Information'),
        }

class idea_vote(osv.osv):
    """ Vote """
    _name = "idea.vote"
    _inherits={'idea.vote.category': "vote_id"}
    _columns = {
        'user_id': fields.many2one('res.users', 'User'),
        'vote_dt': fields.datetime('Posting Date'),
        'idea_id': fields.many2one('idea.idea', 'Idea Id',invisible=True),
        'decision': fields.selection([('yes','Yes'),('no','No'),('maybe','Maybe')],'Voting'),
        'comment': fields.text('Comments'),
        'vote_id': fields.many2one('idea.vote.category', 'Vote ID', invisible=True)
    }
    _defaults = {
        'vote_dt': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': lambda self, cr, uid, ctx: uid,
        'decision': 'yes'
    }

class idea_idea(osv.osv):
    """ Idea """
    _name = "idea.idea"
    _inherit =['mail.thread', 'ir.needaction_mixin']
    
    def _vote_count(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return {}
        res={}
        vote_obj=self.pool.get('idea.vote')
        for idea in self.browse(cr,uid,ids,context=context):
             print idea
             if idea:
                 print uid, ids
                 vote_id=vote_obj.search(cr,uid,[('idea_id','=', idea.id)])
                 res[idea.id]=len(vote_id)
             return res
             print res
         
    _columns = {
        'name': fields.char('Idea Summary', required=True),
        'nbr': fields.integer('nbr'),
        'creator': fields.many2one('res.users', 'Creator'),
        'pst_date': fields.date('Date'),
        'open_date': fields.datetime('Open'),
        'close_date': fields.datetime('Close'),
        'state': fields.selection([('new','New'),('open','Opened'),('close','Accepted'),('cancel','Refused')],'State', track_visibility='onchange'),
        'requirement_id': fields.many2many('idea.requirements', 'res_idea_requirements_rel', 'idea_id','requirement_id',
                                           'Requirement'),
        'category': fields.many2one('idea.category', 'Category'),
        'opened': fields.boolean('Open'),
        'voter': fields.one2many('idea.vote', 'idea_id', 'Vote'),
        'description': fields.text('Description'),
        'parent_idea_category_id': fields.many2one('idea.category', 'Parent Category'),
        'count_votes': fields.function(_vote_count, method=True, String="Number of Votes", type="integer"),
        'email': fields.related('creator','user_email', type="char", string="email", store=False),
    }
    _defaults = {
        'state':'new',
        'pst_date': lambda *a: time.strftime('%Y-%m-%d'),
        'open_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    _order = 'name asc'
    
    _sql_constraints=[('name_creator_unique','unique(name,creator)','Idea Summary and its creator should be unique !!')]
    
    def _check_open_close_date(self,cr,uid,ids,context=None):
        for idea in self.read(cr,uid,ids,['open_date','close_date'],context=context):
            if idea['open_date'] and idea['close_date'] and idea['open_date'] > idea['close_date']:
                return False
        return True
    
    _constraints=[(_check_open_close_date,'Close Time cannot be before Open Time',['open_date','date_time'])]

    def on_change_category(self,cr,uid,ids,category,context=None):
        idea_category_obj=self.pool.get('idea.category').browse(cr,uid,category,context=context)
        print idea_category_obj
        if category:
            parent_idea_category_id=idea_category_obj.parent_id.id
            return {'value':{'parent_idea_category_id':parent_idea_category_id}}
        print {'value':{'parent_idea_category_id':parent_idea_category_id}}
        
    def create(self,cr,uid,vals,context=None):
        if vals['description']==False:
            description1='This is default description'
            vals.update({'description':description1})
        return super(idea_idea, self).create(cr,uid,vals,context=context)

    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('open_date', False):
            vals.update({'opened': True})
        return super(idea_idea, self).write(cr,uid,ids,vals,context=context)
    
    def wkf_act_idea_opened(self,cr,uid,ids):
        self.write(cr, uid, ids, {'state':'open', 'open_date':time.strftime('%Y-%m-%d %H:%M:%S'), 'close_date':None})
        return True
    
    def wkf_act_idea_accepted(self,cr,uid,ids):
        self.write(cr, uid, ids, {'state':'close', 'close_date':time.strftime('%Y-%m-%d %H:%M:%S'), 'opened': False})
        return True
    
class add_fields_in_idea_idea(osv.osv):
    _name='idea.idea'
    _inherit="idea.idea"
    _columns={
           'vote_limit': fields.integer('Maximum vote per user'),}
 
    _defaults = {
        'vote_limit':1,
        }
    
    _sql_constraints=[('vote_limit_positive','check(vote_limit > 0)','Maximum Vote should be greater than zero !!')]
    
class idea_requirements(osv.osv):
    """ Requirements """
    _name = "idea.requirements"
    _columns = {
        'name': fields.char('Requirements')
    }
 
class idea_category(osv.osv):
    """ Category of Idea """
    _name = "idea.category"
    _columns = {
        'name': fields.char('Category Name'),
        'parent_id': fields.many2one('idea.category', 'Parent Category'),
        'child_id': fields.one2many('idea.category', 'parent_id', 'Child Category'),
    }
    