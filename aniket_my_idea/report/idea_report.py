from report import report_sxw
import time
class idea_report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context):
        super(idea_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({'time':time,'get_detail':self.get_detail,'get_total':self.get_total})
      


    def get_detail(self,vote_id):
        result=[]
        self.total_vote=0.00
        if vote_id:
            for v in vote_id:
                res={}
                res['user']=v.user_id.name
                res['comment']=v.comment
                res['vote']=v.vote
                self.total_vote+=float(v.vote)
                result.append(res)
            return result
    
    def get_total(self):
        return self.total_vote   
       
report_sxw.report_sxw('report.idea.information','idea.idea','addons_training/aniket_my_idea/report/idea_report2.rml',parser=idea_report) 