from flask import render_template, Blueprint, request
from report_portal.utils import json_return


from report_portal.apis.detailed_report import (
    open_with_no_scans_in_48_hours,
    assigned_to_driver_no_scan_24,
    open_order_count_by_driver,
    driver_completion_by_hub
)


detailed = Blueprint('detailed', __name__)

# Define decorator function
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,content-type,authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Apply decorator function to all routes
@detailed.after_request
def after_request(response):
    return add_cors_headers(response)

@detailed.route("/detailed/open-no-scan-48/", methods=['POST'])
def open_no_scan_48_rte():
    input_data = request.get_json()
    dc_segment = None
    if 'dc_segment' in input_data and input_data['dc_segment']:
        dc_segment = input_data['dc_segment']
    account_number = None
    if 'account_number' in input_data:
        account_number = input_data['account_number']
    aging_threshold = None
    if 'aging_threshold' in input_data:
        aging_threshold = input_data['aging_threshold']
    report, success, msg = open_with_no_scans_in_48_hours(dc_segment=dc_segment, aging_threshold=aging_threshold, account_number=account_number)
    return json_return(report, success, msg)  

@detailed.route("/detailed/assigned-to-driver-no-scan-24/", methods=[ 'POST'])
def assigned_to_driver_no_scan_24_rte(): 
    input_data = request.get_json()
    dc_segment = None
    if 'dc_segment' in input_data:
        dc_segment = input_data['dc_segment']
    account_number = None
    if 'account_number' in input_data:
        account_number = input_data['account_number']
    aging_threshold = None
    if 'aging_threshold' in input_data:
        aging_threshold = input_data['aging_threshold']
    report, success, msg = assigned_to_driver_no_scan_24(dc_segment=dc_segment, aging_threshold=aging_threshold, account_number=account_number)
    return json_return(report, success, msg)  

@detailed.route("/detailed/open-order-count-by-driver/", methods=['POST'])
def open_order_count_by_driver_rte(): 
    input_data = request.get_json()
    driver_dc = None
    driver_no = None
    if 'driver_dc' in input_data:
        driver_dc = input_data['driver_dc']
    if 'driver_no' in input_data:
        driver_no = input_data['driver_no']
    report, success, msg = open_order_count_by_driver(driver_dc=driver_dc, driver_no=driver_no)
    return json_return(report, success, msg)  

@detailed.route("/detailed/driver-completion/", methods=['POST'])
def driver_completion_by_hub_rte(): 
    input_data = request.get_json()
    driver_center = None
    target_date = None
    driver_type = None
    driver_numbers = None 
    if 'driver_center' in input_data:
        driver_center = input_data['driver_center']
    if 'target_date' in input_data:
        target_date = input_data['target_date']
    if 'driver_type' in input_data:
        driver_type = input_data['driver_type']
    if 'driver_numbers' in input_data: 
        driver_numbers = input_data['driver_numbers']
    report, success, msg = driver_completion_by_hub(
        driver_center=driver_center,
        target_date=target_date, 
        driver_type=driver_type, 
        driver_numbers=driver_numbers
    )
    return json_return(report, success, msg)  