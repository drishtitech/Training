import time
from osv import osv,fields
from report import report_sxw

class sims_report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context):
        super(sims_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({'time':time,'get_details':self.get_details,'get_total':self.get_total})
    
    def get_details(self,marksheet_ids):
        result=[]
        self.total_sore=0
        if marksheet_ids:
            for m in marksheet_ids:
                marksheet_obj = self.pool.get('student.marksheet')
                marksheet_records = marksheet_obj.read(self.cr,self.uid,m.id,['semester','subject1','subject2','subject3','total'])
                res={}
                res['semester'] = marksheet_records['semester']
                res['subject1'] = marksheet_records['subject1']
                res['subject2'] = marksheet_records['subject2']
                res['subject3'] = marksheet_records['subject3']
                res['total'] = marksheet_records['total']
                self.total_vote += int(res['total'])
                result.append(res)
        return result
    
    def get_total(self):
        return self.total_vote
        
report_sxw.report_sxw('report.idea.information','my.idea','addons_training/rahul_SIMS/report/sims_report.rml', parser=sims_report)