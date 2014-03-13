from osv import osv, fields
import time

#Class storing the details about the departments
class dept_details(osv.osv):
    _name = "dept.details"
    
    _columns = {
            'name' : fields.char('Name', required = True)
    }
    
class doctor_details(osv.osv):
    _name = "doctor.details"
    
    _columns = {
            'name' : fields.char('Name', required = True),
            'department' : fields.many2one('dept.details', 'Department', required = True),
            'street1' : fields.char('Address'),
            'street2' : fields.char(' '),
            'city' : fields.char(' '),
            'state' : fields.many2one('res.country.state', ' '),
            'zip' : fields.char(' '),
            'country' : fields.many2one('res.country', ' '),
            'email' : fields.char('Email'),
            'phone' : fields.char('Contact no.')
    }
    
    _order = 'name asc'
    
    _sql_constraints = [
            ('check_name_dept_unique', 'unique(name, department)', 'A department can not have two doctors with the same name')]
    
    def _doctor_details_check_phone(self,cr,uid,ids,context=None):
        for ph in self.read(cr,uid,ids,[],context=context):
            print ph
            if ph['phone'] and ph['phone'].isnumeric():
                print len(str(ph['phone']))
                if len(str(ph['phone']))>10:
                    print 'inside if'
                    return False
            return True
    
    _constraints = [
            (_doctor_details_check_phone,'Phone number should be numeric and should have 10 digits only. Please check',['phone'])]
    
#Class storing the details about the problems
class problem_details(osv.osv):
    _name = "problem.details"
    
    _columns = {
            'name' : fields.char('Name', required = True),
            'dept_id' : fields.many2one('dept.details', 'Department', required = True),
            'doctor_id' : fields.many2one('doctor.details', 'Doctor', required = True),
            'description' : fields.text('Description'),
            'seriousness' : fields.selection([('mild','Mild'),('serious','Serious'),('very serious','Very Serious')], 'Seriousness'),
            'patient_id' : fields.many2one('patient.details', 'Patient')
    }
    
    def create(self,cr,uid,vals,context=None):
        if vals['description'] == False:
            default_description = 'You have not provided any description for the problem of the patient...'
            vals.update({'description' : default_description})
        return super(problem_details,self).create(cr,uid,vals,context=context)
    
    def on_change_dept(self,cr,uid,dept_id,context=None):
        #result=[]
        doc_obj = self.pool.get('doctor.details')
        doctor_records = doc_obj.read(self.cr,self.uid,dept_id,[id])
        print ">>>Doctor Records>>>>>",doctor_records
    
#Class storing the details about the doctors in the hospital.

#Class storing the details about the patients.  
class patient_details(osv.osv):
    _name = "patient.details"
    
    _columns = {
            'name' : fields.char('Name of the patient', required = True),
            'street1' : fields.char('Address'),
            'street2' : fields.char(' '),
            'city' : fields.char(' '),
            'state' : fields.many2one('res.country.state', ' '),
            'pin_code' : fields.char(' '),
            'country' : fields.many2one('res.country', ' '),            
            'email' : fields.char('Email'),
            'phone' : fields.char('Contact no.'),
            'ward_no' : fields.integer('Ward Number'),
            'bed_no' : fields.integer('Bed Number'),
            'problem_id' : fields.one2many('problem.details', 'patient_id', 'Problem')}
    
    _order = 'name asc'
    
    def patient_details_check_phone(self,cr,uid,ids,context=None):
        for ph in self.read(cr,uid,ids,['phone'],context=context):
            if ph['phone'] and ph['phone'].isnumeric():
                if len(ph['phone'])!=10:
                    return False
            return True
    
    _constraints = [
            (patient_details_check_phone,'Phone number should be numeric and should have 10 digits only. Please check',['phone'])]
    
    def patient_details_check_pin(self,cr,uid,ids,context=None):
        for pincode in self.read(cr,uid,ids,['pin_code'],context=context):
            if pincode['pin_code'] and pincode['pin_code'].isnumeric():
                if len(pincode['pin_code'])!=8:
                    return False
            return True
        
    _constraints = [
            (patient_details_check_pin, 'ZIP code should be of 8 digits',['pin_code'])]
