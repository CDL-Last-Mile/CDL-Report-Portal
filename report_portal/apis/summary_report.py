from report_portal.models import (
    OrderDrivers,
    XOrderDrivers,
    Orders,
    XOrders,
    OrderScans,
    Employees,
    DCSegments,
    PortalDistribution,
    PortalSummaryReport,
    PortalSummaryReportType,
    Terminals, 
    ClientMaster
)
from report_portal import db, mail
from sqlalchemy import Date, func
from datetime import datetime, timedelta, date
from flask_mail import Message
from flask import render_template
from report_portal.config import config

import xlsxwriter
import pandas as pd

def get_distribution_email(id):
    recipient = []
    try:
        dbsummary = db.session.query(PortalSummaryReport.distribution_id, PortalDistribution.email, PortalSummaryReportType.portal_summary_report_type_id)
        dbsummary = dbsummary.join(PortalSummaryReportType, PortalSummaryReport.report_type_id == PortalSummaryReportType.portal_summary_report_type_id)
        dbsummary = dbsummary.join(PortalDistribution, PortalSummaryReport.distribution_id == PortalDistribution.portal_distribution_id)
        dbsummary = dbsummary.filter(PortalSummaryReport.portal_summary_report_id == id)
        recipient.append(dbsummary.first()[1])
        if recipient is not None:
            return recipient
    except Exception as e: 
        return e
    return None

def open_with_no_scans_in_48_hours():
    summary = []
    success = False 
    msg = 'Failed'
    try:
        threshold = datetime.now() - timedelta(days=2)
        dbquery = db.session.query(db.func.count(Orders.OrderTrackingID).label('order_count'), Employees.DriverNo.label('driver_no'))
        dbquery = dbquery.join(OrderScans, Orders.OrderTrackingID == OrderScans.OrderTrackingID)
        dbquery = dbquery.join(OrderDrivers, Orders.OrderTrackingID == OrderDrivers.OrderTrackingID, isouter=True)
        dbquery = dbquery.join(Employees, Employees.ID == OrderDrivers.DriverID, isouter=True)
        dbquery = dbquery.filter(Orders.Status == 'N')
        dbquery = dbquery.group_by(Employees.DriverNo)
        dbquery = dbquery.having(func.max(OrderScans.aTimeStamp) <= threshold)
        dbquery = dbquery.order_by(db.asc(Employees.DriverNo))
        summary = [r._asdict() for r in dbquery.all()]
    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}


def unassigned_orders_with_no_daily_scans():
    summary = []
    success = False 
    msg = 'Failed'
    try: 
        threshold = datetime.today() - timedelta(days=1)
        dbfilter = db.session.query(OrderDrivers.OrderTrackingID)
        dbquery = db.session.query(db.func.count(Orders.OrderTrackingID).label('order_count'), DCSegments.Name.label('dc_segment'))
        dbquery = dbquery.join(OrderScans, Orders.OrderTrackingID == OrderScans.OrderTrackingID, isouter=True)
        dbquery = dbquery.join(DCSegments, DCSegments.DCsegmentID == Orders.DCsegmentID)
        dbquery = dbquery.filter(
            ~Orders.OrderTrackingID.in_(dbfilter),
            Orders.Status == 'N' )
        dbquery = dbquery.group_by(DCSegments.Name)
        dbquery = dbquery.having(func.max(OrderScans.aTimeStamp) <= threshold)
        
        summary = [r._asdict() for r in dbquery.all()]
    
    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}
    

def driver_completion_by_hub(): 
    summary = []
    success = False 
    msg = 'Failed'

    try: 
        today = datetime.today()
        today = today.date()
        status_list = ['N', 'D', 'L']
        dbquery = db.session.query(
            Terminals.TerminalID.label('TerminalID'), 
            Terminals.TerminalName, 
            Employees.ID.label('DriverID'),
            Employees.DriverNo, 
            Employees.LastName, 
            Employees.FirstName,
            (db.session.query(db.func.count(XOrderDrivers.OrderTrackingID)).join(XOrders, XOrders.OrderTrackingID == XOrderDrivers.OrderTrackingID).join(ClientMaster, ClientMaster.ClientID == XOrders.ClientID).filter(XOrderDrivers.DriverID == Employees.ID, XOrders.Status == 'N', XOrders.DeliveryTargetTo.cast(Date) == today)
            ).label('Noncomplete_Count'),
            (db.session.query(db.func.count(XOrderDrivers.OrderTrackingID)).join(XOrders, XOrders.OrderTrackingID == XOrderDrivers.OrderTrackingID).join(ClientMaster, ClientMaster.ClientID == XOrders.ClientID).filter(XOrderDrivers.DriverID == Employees.ID, ~XOrders.Status.in_(status_list), XOrders.DeliveryTargetTo.cast(Date) == today)
            ).label('Complete_Count')
        )
        dbquery = dbquery.join(Terminals, Terminals.TerminalID == Employees.TerminalID)
        dbquery = dbquery.filter(Employees.Status == 'A', Employees.Driver == 'Y', Employees.DriverType == 'C')
        dbquery = dbquery.group_by(
            Terminals.TerminalID,
            Terminals.TerminalName,
            Employees.ID,
            Employees.DriverNo,
            Employees.LastName,
            Employees.FirstName)
        dbquery = dbquery.order_by(
            Terminals.TerminalID,
            Terminals.TerminalName,
            Employees.ID,
            Employees.DriverNo,
            Employees.LastName,
            Employees.FirstName)

        summary = [r._asdict() for r in dbquery.all()]




    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}

def unassigned_orders():
    summary = []
    success = False 
    msg = 'Failed'
    try: 
        dbfilter = db.session.query(OrderDrivers.OrderTrackingID)
        dbquery = db.session.query(db.func.count(Orders.OrderTrackingID).label('order_count'), DCSegments.Name.label('dc_segment'))
        dbquery = dbquery.join(DCSegments, DCSegments.DCsegmentID == Orders.DCsegmentID)
        dbquery = dbquery.filter(
            ~Orders.OrderTrackingID.in_(dbfilter),
            Orders.Status == 'N'
        )
        dbquery = dbquery.group_by(DCSegments.Name)
        summary = [r._asdict() for r in dbquery.all()]


    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}


def assigned_to_driver_no_scan_24(): 
    summary = []
    success = False 
    msg = 'Failed'

    try: 
        threshold = datetime.now()
        dbquery = db.session.query(db.func.count(Orders.OrderTrackingID).label('order_count'), Terminals.TerminalName.label('driver_dc'))
        dbquery = dbquery.join(OrderScans, Orders.OrderTrackingID == OrderScans.OrderTrackingID, isouter=True)
        dbquery = dbquery.join(OrderDrivers, Orders.OrderTrackingID == OrderDrivers.OrderTrackingID)
        dbquery = dbquery.join(Employees, OrderDrivers.DriverID == Employees.ID)
        dbquery = dbquery.join(Terminals, Terminals.TerminalID == Employees.TerminalID)
        dbquery = dbquery.filter(Orders.Status == 'N', Employees.DriverType == 'C')
        dbquery = dbquery.group_by(Terminals.TerminalName)
        dbquery = dbquery.having(func.max(OrderScans.aTimeStamp) <= threshold)
        summary = [r._asdict() for r in dbquery.all()]

    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}

def orders_per_weekly_address(): 
    summary = []
    success = False 
    msg = 'Failed'

    try: 
        start = datetime.now() - timedelta(days=8)
        start = start.date()
        end = datetime.now() - timedelta(days=1)
        end = end.date()
        dbquery = db.session.query(
            db.func.count(Orders.OrderTrackingID).label('count'), 
            Orders.DStreet.label('street'), 
            Orders.DCity.label('city'),
            Orders.DState.label('state'),
            db.func.left(Orders.DZip, 5).label('zip'))
        dbquery = dbquery.filter(Orders.PODcompletion.cast(Date).between(start, end))
        dbquery = dbquery.group_by(Orders.DStreet, Orders.DCity, Orders.DState, db.func.left(Orders.DZip, 5))
        dbquery = dbquery.order_by(db.desc('count'))
        summary = [r._asdict() for r in dbquery.all()]

    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}


def per_financial_orders(): 
    summary = []
    success = False 
    msg = 'Failed'

    try: 
        yesterday = datetime.now() - timedelta(days=1)
        last_week = datetime.now() - timedelta(days=8)
        blocked_account_nos = ['511', '451', '452', '679','480', '295', '195', '6195','6451', '6452', '6679', '6913','725', '11111', '11112', '11113','11114', '11115', '11116', '11117','22222', '66666', '10511']
        dbquery = db.session.query(
            ClientMaster.AccountNo.label('account_number'),
            db.func.count(XOrders.OrderTrackingID).label('order_count'),
            db.func.sum(XOrders.sPieces).label('total_package_count'), 
            db.func.sum(XOrders.GrandTotal).label('total_grand_total'), 
            db.func.sum(XOrders.OrderCharge).label('total_base_charge'), 
            db.func.sum(XOrders.PackageCharge).label('total_package_charge'),
            db.func.sum(XOrders.WeightCharge).label('total_weight_charge'), 
            db.func.sum(XOrders.TotalExtras).label('total_extra_charge'), 
            db.func.sum(XOrders.TotalSurcharges).label('total_surcharges'),
            db.func.sum(XOrderDrivers.DrvCommTotal).label('total_driver_commission')
            )
        dbquery = dbquery.join(ClientMaster, XOrders.ClientID == ClientMaster.ClientID)
        dbquery = dbquery.join(XOrderDrivers, XOrders.OrderTrackingID == XOrderDrivers.OrderTrackingID)
        dbquery = dbquery.filter(XOrders.PODcompletion.cast(Date) > last_week )
        dbquery = dbquery.filter(XOrders.PODcompletion.cast(Date) < yesterday)
        dbquery = dbquery.filter(~ClientMaster.AccountNo.in_(blocked_account_nos))
        dbquery = dbquery.group_by(db.func.rollup(ClientMaster.AccountNo))
        summary = [r._asdict() for r in dbquery.all()]

    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}


def dail_delivery_totals():
    summary = []
    success = False 
    msg = 'Failed'
    try: 
        start = datetime.now() - timedelta(days=8)
        start = start.date()
        end = datetime.now() - timedelta(days=1)
        end = end.date()
        dbquery = db.session.query(db.func.count(XOrders.OrderTrackingID).label('count'), XOrders.PODcompletion.cast(Date).label('completion_date'))
        dbquery = dbquery.filter(XOrders.PODcompletion.cast(Date).between(start, end))
        dbquery = dbquery.group_by(XOrders.PODcompletion.cast(Date))
        dbquery = dbquery.order_by(XOrders.PODcompletion.cast(Date))
        summary = [r._asdict() for r in dbquery.all()]
    except Exception as e: 
        msg = e
    return {'data': summary, 'count': len(summary)}