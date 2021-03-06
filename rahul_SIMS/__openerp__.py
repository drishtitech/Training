# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Rahul SIMS',
    'version': '1.0',
    'category': 'Tools',
    'description': """
SIMS (Student Information Management System)
=================================================================

This application allows to store information about the student and his progress semester wise.
""",
    'author': 'DrishtiTech',
    'depends': ['mail'],
    'website': 'http://openerp.com',
    'summary': 'Rahul SIMS',
    'sequence': 9,
    'data': ['wizard/create_marksheet_view.xml','sims_view.xml','sims_workflow.xml','sims_report_view.xml'],
   
   
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: