import time
from report import report_sxw

class idea_report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context):
        super(idea_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({'time':time, 'get_detail':self.get_detail, 'get_total':self.get_total})
        
    def get_detail(self, voter):
        result=[]
        self.total_vote=0
        if voter:
            for v in voter:
                res={}
                res['user']=v.user_id.name
                res['comment']=v.comment
                res['decision']=v.decision
                self.total_vote += 1
                result.append(res)
            return result
    
    def get_total(self):
        return self.total_vote
        
report_sxw.report_sxw('report.idea.information','idea.idea','addons_training/nisha_idea/reports/idea_report.rml',parser=idea_report)
       