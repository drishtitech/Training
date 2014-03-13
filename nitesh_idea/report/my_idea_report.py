import time
from report import report_sxw

class idea_report(report_sxw.rml_parse): # rml.parse is by default parser
    def __init__(self,cr,uid,name,context): #idea_report is custom parser
        super(idea_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({'time':time, 'get_detail':self.get_detail, 'get_total':self.get_total,'get_count':self.get_count})
    
    
    def get_detail(self,vote_ids):
        result=[]
        self.count=0
        self.total_decision=0.00
        if vote_ids:
            for v in vote_ids:
                res={}
                res['user_id']=v.user_id.name
                res['comments']=v.comments
                res['decision']=v.decision
                self.total_decision += float(v.decision)
                self.count += 1
                result.append(res)
            print '<<<<<< RESULT  >>>>>>',result    
            return result
    
    
    def get_total(self):
        return self.total_decision
    
    def get_count(self):
        return self.count
    
    #calling report_sxw method of report_sxw class & passing args 
    #report.idea.information is name of report in xml file
    #idea.idea is model name
    # then path of rml
    #custom parser we want to use
report_sxw.report_sxw('report.idea.information','idea.idea','my_idea/report/my_idea_report.rml',parser=idea_report)