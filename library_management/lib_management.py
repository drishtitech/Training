from openerp.osv import osv
from openerp.osv import fields
import time, datetime

class book_member(osv.osv):
    """ Members """
    _name = "book.member"
    _columns = {
        'name': fields.char('Member Name'),
    } 

class book_user(osv.osv):
    """ Book Register """
    _name = "book.user"
    _inherits= {'book.member': "member_id"}
    _columns = {
        'book_id': fields.many2one('book.book', 'Book', invisible=True),
        'check_out': fields.date('Check Out'),
        'comment': fields.text('Comments'),
        'check_in': fields.date('Check In'),
        'member_id': fields.many2one('book.member', 'Member', invisible=True),
    }
    
    _defaults = {
        'check_out': lambda *a: time.strftime('%Y-%m-%d'),
    } 
    
class book_book(osv.osv):
    """ Library Books """
    _name = "book.book"
    _inherit =['mail.thread', 'ir.needaction_mixin']
      
    _columns = {
        'name': fields.char('Book Name', required=True),
        'category': fields.many2one('book.category', 'Category'),
        'no_of_copies': fields.integer('No of Copies'),
        'available': fields.boolean('Availability'),
        'user': fields.one2many('book.user', 'book_id', 'Member'),
        'author': fields.char('Book Author'),
        'publication': fields.char('Publication'),
    }
    _defaults = {
        'no_of_copies': 0
    }
    
    _order = 'name asc'
    
    _sql_constraints=[('name_author_unique','unique(name,author)','This book already exists !!')]
        
class book_category(osv.osv):
    """ Book Category """
    _name = "book.category"
    _columns = {
        'name': fields.char('Category Name'),
        'parent_id': fields.many2one('book.category', 'Parent Category'),
        'child_id': fields.one2many('book.category', 'parent_id', 'Child Category'),
    }
