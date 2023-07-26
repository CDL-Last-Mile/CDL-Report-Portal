from flask import render_template, request, Blueprint
from report_portal.utils import json_return


from report_portal.apis.report import (
    add_portal_summary_report,
    update_portal_summary_report,
    get_portal_summary_report, 
    add_portal_summary_report_type, 
    update_portal_summary_report_type, 
    get_portal_summary_report_type
)



report = Blueprint('report', __name__)

# Define decorator function
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,content-type,authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Apply decorator function to all routes
@report.after_request
def after_request(response):
    return add_cors_headers(response)

@report.route("/report/add/", methods=['POST'])
def add_portal_summary_report_rte():
    input_data = request.get_json()
    portal_report, success, msg = add_portal_summary_report(input_data['portal_data']) 
    return json_return(portal_report, success, msg)

@report.route("/report/update/", methods=['POST'])
def update_portal_summary_report_rte():
    input_data = request.get_json()
    portal_report, success, msg = update_portal_summary_report(input_data['portal_data']) 
    return json_return(portal_report, success, msg)


@report.route("/report/", methods=['GET'])
def get_portal_summary_report_rte():
    report, success, msg = get_portal_summary_report()
    return json_return(report, success, msg)

@report.route("/report-type/add/", methods=['POST'])
def add_portal_summary_report_type_rte():
    input_data = request.get_json()
    portal_report, success, msg = add_portal_summary_report_type(input_data['portal_data']) 
    return json_return(portal_report, success, msg)

@report.route("/report-type/update/", methods=['POST'])
def update_portal_summary_report_type_rte():
    input_data = request.get_json()
    portal_report, success, msg = update_portal_summary_report_type(input_data['portal_data']) 
    return json_return(portal_report, success, msg)


@report.route("/report/report-type/", methods=['GET'])
def get_portal_summary_report_type_rte():
    report, success, msg = get_portal_summary_report_type()
    return json_return(report, success, msg)



