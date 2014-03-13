import time
from osv import osv,fields
from report import report_sxw

class idea_report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context):
        super(idea_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({'time':time,'get_details':self.get_details,'get_total':self.get_total})
    
    def get_details(self,vote_ids):
        result=[]
        self.total_vote=0
        if vote_ids:
            for v in vote_ids:
                vote_obj = self.pool.get('idea.vote')
                vote_records = vote_obj.read(self.cr,self.uid,v.id,['user_id','comment','decision'])
                res={}
                u = vote_records['user_id']
                res['user'] = u[1]
                res['comment'] = vote_records['comment']
                res['value'] = vote_records['decision']
                self.total_vote += int(res['value'])
                result.append(res)
        return result
    
    def get_total(self):
        return self.total_vote
        
report_sxw.report_sxw('report.idea.information','my.idea','addons_training/rahul_idea/report/idea_report.rml', parser=idea_report)