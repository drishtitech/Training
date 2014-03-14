from osv import osv, fields
import time
import datetime

class student_marksheet(osv.osv):
    
    _name = "student.marksheet"
    
    def total_score(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return {}
        res={}
        for score in self.browse(cr,uid,ids,context=context):
            if score:
                result = score.subject1 + score.subject2 + score.subject3
                res[score.id] = result
        return res
    
    def check_status(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return{}
        res={}
        for rec in self.browse(cr,uid,ids,context=None):
            if rec:
                avg = rec.total/3
                if avg >= 50.00:
                    st = 'Pass'
                else:
                    st = 'Fail'
                res[rec.id] = st
        return res
    
    _columns = {
        'student_id' : fields.many2one('student.student','Student'),
        'semester' : fields.selection([('sem1','Semester 1'),('sem2','Semester 2'),('sem3','Semester 3'),('sem4','Semester 4')],'Semester'),
        'subject1' : fields.float('Score of Subject 1'),
        'subject2' : fields.float('Score of subject 2'),
        'subject3' : fields.float('Score of subject 3'),
        'total' : fields.function(total_score, method=True, string="Total Score", type="float"),
        'status' : fields.function(check_status, method=True, string="Status", type="char")
    }
    
    def check_subject(self,cr,uid,ids,context=None):
        for record in self.read(cr,uid,ids,[],context=context):
            if record['subject1']  and record['subject2'] and record['subject3']:
                if ((record['subject1'] > 100.00) or (record['subject2'] > 100.00) or (record['subject3'] > 100.00)):
                    return False
            return True
    
    _constraints = [
            (check_subject,'Maximum marks allowed for each subject is 100',['subject1','subject2','subject3'])]
    
class student_details(osv.osv):
    
    _name = "student.student"
    
    def calculate_age(self,cr,uid,ids,name,arg,context=None):
        if not ids:
            return {}
        res={}
        for student in self.browse(cr,uid,ids,context=context):
            if student:
                dob = datetime.datetime.strptime(student.birth_date, '%Y-%m-%d')
                doa = datetime.datetime.strptime(student.admit_date, '%Y-%m-%d')
                result = doa - dob
                res[student.id] = result.days/365
        return res

    _columns={
        'name' : fields.char('Student Name', size = 50, required = True),
        'gender' : fields.selection([('male','Male'),('female','Female')], 'Gender', required = True),
        'birth_date' : fields.date('Date of Birth', required = True),
        'admit_date' : fields.date('Date of Admission', required = True),
        'age' : fields.function(calculate_age, method=True, string="Age", type="integer"),
        'street1' : fields.char('Address'),
        'street2' : fields.char(' '),
        'city' : fields.char(' '),
        'state_name' : fields.many2one('res.country.state', ' '),
        'pin_code' : fields.char(' '),
        'country' : fields.many2one('res.country', ' '),
        'email' : fields.char('Email'),
        'phone' : fields.char('Contact no.'),
        'state': fields.selection([('sem1','Semester 1'),('sem2','Semester 2'),('sem3','Semester 3'),('sem4','Semester 4')],'Semester'),
        'marksheet_id' : fields.one2many('student.marksheet', 'student_id', 'Student Marksheet')
        }
    
    _defaults = {
        'gender' : 'male',
        'state' : 'sem1'
    }
    
    def check_birth_date(self,cr,uid,ids,context=None):
        for dob in self.read(cr,uid,ids,[],context=context):
            if dob['birth_date'] and dob['birth_date'] >= time.strftime('%Y-%m-%d'):
                return False
            return True
    
    _constraints = [
            (check_birth_date,'Date of Birth must be before today\'s date',['birth_date'])]
    
    def check_admit_date(self,cr,uid,ids,context=None):
        for doa in self.read(cr,uid,ids,[],context=context):
            if doa['admit_date'] and doa['birth_date'] and (doa['admit_date'] < doa['birth_date'] or doa['admit_date'] > time.strftime('%Y-%m-%s')):
                return False
            return True
    
    _constraints = [
            (check_admit_date,'Date of Admission must be before today\'s date',['admit_date','birth_date'])]
    
    #Workflow's Activity Methods
    def sem1_sem2(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'sem2'})
        return True
    
    def sem2_sem3(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'sem3'})
        return True
    
    def sem3_sem4(self,cr,uid,ids):
        self.write(cr,uid,ids,{'state':'sem4'})
        return True
