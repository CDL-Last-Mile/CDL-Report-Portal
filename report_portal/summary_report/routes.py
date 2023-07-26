from flask import render_template, Blueprint, request

from report_portal.apis.summary_report import (
    open_with_no_scans_in_48_hours, 
    unassigned_orders_with_no_daily_scans, 
    driver_completion_by_hub, 
    unassigned_orders,
    assigned_to_driver_no_scan_24, 
    orders_per_weekly_address, 
    per_financial_orders, 
    dail_delivery_totals
)

summary = Blueprint('summary', __name__)

# Define decorator function
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,content-type,authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Apply decorator function to all routes
@summary.after_request
def after_request(response):
    return add_cors_headers(response)

@summary.route("/summary/open-no-scan-48", methods=['GET'])
def open_no_scan_48_rte():
    return open_with_no_scans_in_48_hours()


@summary.route("/summary/unassigned-no-scan-24", methods=['GET'])
def unassigned_no_scan_24_rte(): 
    return unassigned_orders_with_no_daily_scans()


@summary.route("/summary/driver-completion-by-hub", methods=['GET'])
def driver_completion_by_hub_rte(): 
    return driver_completion_by_hub()


@summary.route("/summary/unassigned-orders", methods=['GET'])
def unassigned_orders_rte(): 
    return unassigned_orders()

@summary.route("/summary/assigned-to-driver-no-scan-24")
def assigned_to_driver_no_scan_24_rte(): 
    return assigned_to_driver_no_scan_24()

@summary.route("/summary/orders-per-weekly-address", methods=['GET'])
def orders_per_weekly_address_rte():
    return orders_per_weekly_address()


@summary.route("/summary/per-order-financials", methods=['GET'])
def per_financial_orders_rte(): 
    return per_financial_orders()


@summary.route("/summary/daily-delivery-totals", methods=['GET'])
def dail_delivery_totals_rte():
    return dail_delivery_totals()
