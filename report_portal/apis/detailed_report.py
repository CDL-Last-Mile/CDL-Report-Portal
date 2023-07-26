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
from sqlalchemy import Date, func, text
from datetime import datetime, timedelta, date
from flask_mail import Message
from flask import render_template
from report_portal.config import config

import xlsxwriter
import pandas as pd


def open_with_no_scans_in_48_hours(dc_segment=None, aging_threshold=None, account_number=None):
    report = []
    success = False 
    msg = 'Failed'
    try:
        threshold = datetime.now() - timedelta(days=3)
        if aging_threshold: 
            threshold = datetime.strptime(aging_threshold, "%Y-%m-%d").date()
        dbquery = db.session.query(
                        Orders.OrderTrackingID.label('order_tracking_id'),
                        Employees.DriverNo.label('driver_no'),
                        func.DATEDIFF(text('day'), func.MAX(func.DISTINCT(OrderScans.aTimeStamp)), func.current_date()).label('days_old')
                    ).join(
                        OrderScans,
                        Orders.OrderTrackingID == OrderScans.OrderTrackingID
                    ).join(
                        ClientMaster, 
                        Orders.ClientID == ClientMaster.ClientID
                    ).join(
                        DCSegments, 
                        Orders.DCsegmentID == DCSegments.DCsegmentID
                    ).outerjoin(
                        OrderDrivers,
                        Orders.OrderTrackingID == OrderDrivers.OrderTrackingID
                    ).outerjoin(
                        Employees,
                        Employees.ID == OrderDrivers.DriverID
                    ).filter(
                        Orders.Status == 'N',
                        OrderScans.aTimeStamp <= threshold
                    )
        if dc_segment: 
            dbquery = dbquery.filter(Orders.DCsegmentID.in_(dc_segment))
        if account_number: 
            dbquery = dbquery.filter(ClientMaster.AccountNo.in_(account_number))
        dbquery = dbquery.group_by(
                        Orders.OrderTrackingID,
                        Employees.DriverNo
                    ).order_by(
                        Employees.DriverNo.asc()
                    )

        report = [r._asdict() for r in dbquery.all()]
        for r in report: 
            if r['driver_no'] is None: 
                r['driver_no'] = 'Unassigned'
        success = True 
        msg = 'Open With No Scans in 48 Hours Report Generated'
    except Exception as e: 
        msg = str(e)
    return report, success, msg


def assigned_to_driver_no_scan_24(dc_segment=None, aging_threshold=None, account_number=None): 
    report = []
    success = False 
    msg = 'Failed'


    try: 
        threshold = datetime.today() - timedelta(days=1)
        if aging_threshold: 
            threshold = datetime.strptime(aging_threshold, "%Y-%m-%d").date()
        dbquery = db.session.query(
                    Orders.OrderTrackingID.label('order_tracking_id'),
                    DCSegments.Name.label('driver_dc'), 
                    func.DATEDIFF(text('day'), func.MAX(func.DISTINCT(OrderScans.aTimeStamp)), func.current_date()).label('days_old')
                ).outerjoin(
                    OrderScans,
                    Orders.OrderTrackingID == OrderScans.OrderTrackingID
                ).join(
                    OrderDrivers,
                    Orders.OrderTrackingID == OrderDrivers.OrderTrackingID
                ).join(
                    ClientMaster, 
                    Orders.ClientID == ClientMaster.ClientID
                ).join(
                    DCSegments, 
                    Orders.DCsegmentID == DCSegments.DCsegmentID
                ).join(
                    Employees,
                    OrderDrivers.DriverID == Employees.ID
                ).filter(
                    Orders.Status == 'N',
                    Employees.DriverType == 'C',
                    OrderScans.aTimeStamp <= threshold
                )
        if dc_segment: 
            dbquery = dbquery.filter(Orders.DCsegmentID.in_(dc_segment))
        if account_number: 
            dbquery = dbquery.filter(ClientMaster.AccountNo.in_(account_number))
        dbquery = dbquery.group_by(
                        Orders.OrderTrackingID,
                        DCSegments.Name, 
                    ).order_by(
                        DCSegments.Name.asc()
                    )

        report = [r._asdict() for r in dbquery.all()]
        success = True 
        msg = 'Assigned To Driver With No Scan in 24 Hours Report Generated'
    except Exception as e: 
        msg = str(e)
    return report, success, msg


def open_order_count_by_driver(driver_no=None, driver_dc=None):
    report = []
    success = False 
    msg = 'Failed'

    try:    

        dbquery = db.session.query(db.func.count(Orders.OrderTrackingID).label('order_count'), Employees.DriverNo.label('driver_no'), Terminals.TerminalName.label('driver_dc'))
        dbquery = dbquery.join(OrderDrivers, Orders.OrderTrackingID == OrderDrivers.OrderTrackingID)
        dbquery = dbquery.join(Employees, Employees.ID == OrderDrivers.DriverID)
        dbquery = dbquery.join(Terminals, Terminals.TerminalID == Employees.TerminalID)
        dbquery = dbquery.filter(Employees.DriverType == 'C', Orders.Status == 'N')
        if driver_no: 
            dbquery = dbquery.filter(Employees.DriverNo.in_(driver_no))
        if driver_dc: 
            dbquery = dbquery.filter(Terminals.TerminalID.in_(driver_dc))
        dbquery = dbquery.group_by(Employees.DriverNo, Terminals.TerminalName)
        dbquery = dbquery.order_by(db.asc(Employees.DriverNo))
        report = [r._asdict() for r in dbquery.all()]
        success = True 
        msg ='Open Orders Count By Driver Report Generated'
    except Exception as e: 
        msg = str(e)
    return report, success, msg

def driver_completion_by_hub(
    driver_center=None,
    target_date=None, 
    driver_type=None, 
    driver_numbers=None
    ): 
    report = []
    success = False 
    msg = 'Failed'

    try: 
        today = datetime.today()
        date_filter = today.date()
        if target_date: 
            date_filter = datetime.strptime(target_date, '%Y-%m-%d').date()
        status_list = ['N', 'D', 'L']
        default_driver_type = 'C'
        if driver_type: 
            default_driver_type = driver_type
        dbquery = db.session.query(
            Terminals.TerminalID.label('TerminalID'), 
            Terminals.TerminalName.label('terminal_name'), 
            Employees.ID.label('driver_id'),
            Employees.DriverNo.label('driver_no'), 
            Employees.LastName.label('last_name'), 
            Employees.FirstName.label('first_name'),
            (db.session.query(db.func.count(XOrderDrivers.OrderTrackingID)).join(XOrders, XOrders.OrderTrackingID == XOrderDrivers.OrderTrackingID).join(ClientMaster, ClientMaster.ClientID == XOrders.ClientID).filter(XOrderDrivers.DriverID == Employees.ID, XOrders.Status == 'N', XOrders.DeliveryTargetTo.cast(Date) == date_filter)
            ).label('noncomplete_count'),
            (db.session.query(db.func.count(XOrderDrivers.OrderTrackingID)).join(XOrders, XOrders.OrderTrackingID == XOrderDrivers.OrderTrackingID).join(ClientMaster, ClientMaster.ClientID == XOrders.ClientID).filter(XOrderDrivers.DriverID == Employees.ID, ~XOrders.Status.in_(status_list), XOrders.DeliveryTargetTo.cast(Date) == date_filter)
            ).label('complete_count')
        )
        dbquery = dbquery.join(Terminals, Terminals.TerminalID == Employees.TerminalID)
        dbquery = dbquery.filter(Employees.Status == 'A', Employees.Driver == 'Y')
        dbquery = dbquery.filter(Employees.DriverType == default_driver_type)
        if driver_center: 
            dbquery = dbquery.filter(Terminals.TerminalID.in_(driver_center))
        if driver_numbers: 
            dbquery = dbquery.filter(Employees.DriverNo.in_(driver_numbers))
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

        report = [r._asdict() for r in dbquery.all()]
        success = True
        msg = 'Driver Completion By Hub Report Generated Successfully'
    except Exception as e: 
        msg = str(e)
    return report, success, msg