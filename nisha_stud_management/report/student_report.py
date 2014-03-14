import time
from report import report_sxw

class student_report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context):
        super(student_report,self).__init__(cr,uid,name,context)
        self.localcontext.update({'time':time, 'get_detail':self.get_detail, 'get_total':self.get_total})
        
    def get_detail(self, stud_marks):
        result=[]
        self.total_marks=0
        if stud_marks:
            for s in stud_marks:
                res={}
                res['english']=v.sub1
                res['maths']=v.sub2
                res['science']=v.sub3
                res['comment']=v.comment
                self.total_marks = float(v.sub1+v.sub2+v.sub3)
                result.append(res)
            return result
    
    def get_total(self):
        return self.total_marks
        
report_sxw.report_sxw('report.student.information','student.student','addons_training/nisha_stud_management/report/student_report.rml',parser=student_report)
       