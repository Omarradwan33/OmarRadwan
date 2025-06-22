from odoo import models, fields, api  # type: ignore


class Doctor(models.Model):
    _name = "doctors"
    _description = "Doctor Record"

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Binary(string="Doctor Image")
    patient_ids = fields.Many2many("hospital.patient", string="Patients")
    department_id = fields.Many2one('hospital.department' , string="Department")
    name = fields.Char(string="Name", compute="_compute_name" , default="New Doctor")
    specialization = fields.Text(string="Specialization")



    @api.depends('first_name' , 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = (f"Dr. {rec.first_name} {rec.last_name}")