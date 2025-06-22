from odoo import models, fields, api  # type: ignore
from odoo.exceptions import ValidationError # type: ignore


class PatientTransferWizard(models.TransientModel):
    _name = 'hospital.patient.transfer.wizard'
    _description = 'Transfer Patients to Another Department'

    new_department_id = fields.Many2one(
        'hospital.department', string='New Department', required=True,
        domain="[('state', '=', 'open')]"
    )
    patient_ids = fields.Many2many(
        'hospital.patient', string='Patients',
        domain="[('department_id', '!=', new_department_id)]"
    )

    def action_transfer(self):
        for patient in self.patient_ids:
            if patient.department_id.id == self.new_department_id.id:
                raise ValidationError(f"Patient {patient.name} is already in the selected department.")

            old_department = patient.department_id.name or "Unknown"
            patient.department_id = self.new_department_id
