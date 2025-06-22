import json
import math
from urllib.parse import parse_qs
from odoo import http # type: ignore
from odoo.http import request, Response  # type: ignore


def valid_response(data, pagination_info, status):
    response_body = {
        "message": "Successful",
        "data": data,
    }
    if pagination_info:
        response_body["pagination_info"] = pagination_info
    return request.make_json_response(response_body, status=status)

def invalid_response(error, status):
    response_body = {
        "error": error
    }
    return request.make_json_response(response_body, status=status)


class HospitalPatientApi(http.Controller):
    @http.route('/v1/hospital/patient', auth='none', methods=['POST'], type="http", csrf=False)
    def post_patient(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("first_name") or not vals.get("last_name"):
            return request.make_json_response(
                {
                    "status": "error",
                    "message": "first_name and last_name are required",
                },
                status=400,
            )
        try:
            patient = request.env['hospital.patient'].sudo().create(vals)
            if patient:
                return request.make_json_response(
                    {
                        "status": "success",
                        "message": "Patient created successfully",
                        "patient_id": patient.id,
                    },
                    status=200,
                )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )

    @http.route('/v1/hospital/patient/<int:id>', method=["PUT"], auth='none', type="http", csrf=False)
    def update_patient(self, id):
        try:
            patient_id = request.env["hospital.patient"].sudo().search([("id", "=", id)])
            if not patient_id:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "Patient not found",
                    },
                    status=404,
                )
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            patient_id.write(vals)
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Patient updated successfully",
                },
                status=200,
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )



    @http.route('/v1/hospital/patient/<int:id>', method=["DELETE"], auth='none', type="http", csrf=False)
    def delete_patient(self, id):
        try:
            patient_id = request.env["hospital.patient"].sudo().search([("id", "=", id)])
            if not patient_id:
                return request.make_json_response(
                    {
                        "status": "error",
                        "message": "Patient not found",
                    },
                    status=404,
                )
            patient_id.unlink()
            return request.make_json_response(
                {
                    "status": "success",
                    "message": "Patient deleted successfully",
                },
                status=200,
            )
        except Exception as error:
            return request.make_json_response(
                {
                    "status": "error",
                    "message": str(error),
                },
                status=400,
            )





    @http.route('/v1/hospital/patient/<int:hospital_patient_id>', methods=["GET"], auth='none', type="http", csrf=False)
    def get_patient(self, hospital_patient_id):
        try:
            patient_id = request.env["hospital.patient"].sudo().browse(hospital_patient_id)

            if not patient_id.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Patient not found"
                }, status=404)

            return request.make_json_response({
                "status": "success",
                "data": {
                    "id": patient_id.id,
                    "name": patient_id.name,
                    "ref": patient_id.reference
                }
            }, status=200)

        except Exception as e:
            return request.make_json_response({
                "status": "error",
                "message": str(e)
            }, status=400)