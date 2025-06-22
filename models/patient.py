from email.policy import default

from odoo import api,fields , models
from odoo.tools.populate import compute


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread' , 'mail.activity.mixin']
    _description = 'Patient Master'




    reference = fields.Char(string="Reference", default="New")
    name = fields.Char(string="Name" , required=1 , tracking=True , compute='_compute_name' , default="Name")
    first_name= fields.Text(string="First Name")
    last_name= fields.Text(string="Last Name")
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Text(string="Age")
    gender = fields.Selection([('male','Male') , ('female','Female')] , string="Gender", tracking=True)
    phone = fields.Char(string="Phone")
    telephone = fields.Char(string="Telephone")
    img = fields.Image(string="Image")
    street = fields.Char(default="Street")
    city = fields.Char(default="City")
    state = fields.Char(default="State/Province")
    country = fields.Char(default="Country")
    email=fields.Text(string="Email")
    government_identity = fields.Char(string="Government Identity")
    marital_status = fields.Selection([('married','Married') , ('single','Single') , ('divorce','Divorce')])
    address = fields.Text(string="Address")

    #ralations
    doctor_ids = fields.Many2many("doctors",string="Doctors")
    # partner_id = fields.Many2one('res.partner', string='Partner', auto_join=True)
    department_id = fields.Many2one("hospital.department",string="Department",required=True,domain="[('state', '=', 'open')]")



    #hospital information
    blood_type = fields.Char(string="Blood Type")
    death_registration = fields.Boolean(string="Death Registration")
    date_of_death = fields.Date(string="Date Of Death")
    #Clinical assessment
    height = fields.Float(string="Height")
    weight=fields.Float(string="Weight")
    blood_pressure = fields.Char(string="Blood Pressure")
    spo2 = fields.Text(string="Spo2")
    symptoms = fields.Text(string="Symptoms")
    diagnosis = fields.Text(string="Diagnosis")

    _sql_constrains = [("unique_email", "unique(email)", "Email must be unique")]




    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = (f"{rec.first_name} {rec.last_name}")



    #add reference
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.reference == 'New':
            res.reference = self.env['ir.sequence'].next_by_code('hospital.patient')
        return res




