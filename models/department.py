from email.policy import default

from odoo import api,fields , models
from odoo.tools.populate import compute


class Department(models.Model):
    _name = 'hospital.department'
    _inherit = ['mail.thread']
    _description = 'Hospital Department'

    patient_ids = fields.One2many("hospital.patient", "department_id", string="Patients")
    doctor_ids = fields.One2many("doctors" , "department_id" , string="Doctors")
    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(string="Capacity")
    state = fields.Selection(
        [("open", "Open"), ("closed", "Closed")],
        string="Status",
        default="open",
        required=True,
    )

    def open_transfer_wizard(self):
        patients = self.env['hospital.patient'].search([('department_id', '=', self.id)])
        return {
            "type": "ir.actions.act_window",
            "res_model": "hospital.patient.transfer.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_patient_ids": [(6, 0, patients.ids)]},
        }