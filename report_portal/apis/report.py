from report_portal.models import PortalSummaryReport, PortalSummaryReportType
from report_portal import db
from datetime import datetime




def add_portal_summary_report(portal_data):
    portal_summary_report = []
    success = False 
    msg = ''
    try:
        new_portal_summary_report = PortalSummaryReport()
        new_portal_summary_report.report_type_id = portal_data['report_type_id']
        new_portal_summary_report.distribution_id = portal_data['distribution_id']
        new_portal_summary_report.report_time = portal_data['report_time']
        new_portal_summary_report.report_frequency = portal_data['report_frequency']
        new_portal_summary_report.report_url = "http://localhost/reportportalserver/report-portal/summary/send-report?distributionid=" + portal_data['distribution_id'] + "&reportid="+ portal_data['report_type_id']
        new_portal_summary_report.date_created = datetime.now()
        new_portal_summary_report.active = 1
        db.session.add(new_portal_summary_report)
        db.session.commit()
        portal_summary_report, success, msg = get_portal_summary_report()
        msg = 'Report Summary added'
    except Exception as e: 
        print(e)
        msg = e
    return portal_summary_report, success, msg 

def update_portal_summary_report(portal_data):
    portal_summary_report = []
    success = False 
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalSummaryReport.portal_summary_report_id, 
            PortalSummaryReport.report_type_id,
            PortalSummaryReport.distribution_id,
            PortalSummaryReport.report_time,
            PortalSummaryReport.report_frequency,
            PortalSummaryReport.report_url,
            PortalSummaryReport.active,
            PortalSummaryReport.date_modified)
        dbquery = dbquery.filter(PortalSummaryReport.portal_summary_report_id == portal_data['portal_summary_report_id'])
        if dbquery: 
            dbquery = dbquery.update({
                'active': portal_data['active'], 
                'report_frequency': portal_data['report_frequency'], 
                'report_url': "http://localhost/reportportalserver/report-portal/summary/send-report?distributionid=" + portal_data['distribution_id'] + "&reportid="+ portal_data['report_type_id'],
                'report_time':portal_data['report_time'],
                'distribution_id': portal_data['distribution_id'], 
                'report_type_id': portal_data['report_type_id']})
            db.session.commit()
            portal_summary_report, success, msg = get_portal_summary_report()
            msg = 'User Type updated'
    except Exception as e: 
        print(e)
        msg = e 
    return portal_summary_report, success, msg

def get_portal_summary_report(): 
    portal_summary_report = []
    success = False 
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalSummaryReport.portal_summary_report_id, 
            PortalSummaryReport.report_type_id,
            PortalSummaryReport.distribution_id,
            PortalSummaryReport.report_time,
            PortalSummaryReport.report_frequency,
            PortalSummaryReport.report_url,
            PortalSummaryReport.active,
            PortalSummaryReport.date_modified)
        portal_summary_report =  [r._asdict() for r in dbquery.all()]
        for report in portal_summary_report: 
            report['report_time'] = str(report['report_time'])
        success = True 
        msg = "Report Portal Summary retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return portal_summary_report, success, msg

def add_portal_summary_report_type(portal_data):
    portal_summary_report = []
    success = False 
    msg = ''
    try:
        new_portal_summary_report = PortalSummaryReportType()
        new_portal_summary_report.report_name = portal_data['report_name']
        new_portal_summary_report.date_created = datetime.now()
        new_portal_summary_report.active = 1
        db.session.add(new_portal_summary_report)
        db.session.commit()
        portal_summary_report, success, msg = get_portal_summary_report_type()
        msg = 'Report Summary Type added'
    except Exception as e: 
        print(e)
        msg = e
    return portal_summary_report, success, msg 

def update_portal_summary_report_type(portal_data):
    portal_summary_report = []
    success = False 
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalSummaryReportType.portal_summary_report_type_id, 
            PortalSummaryReportType.report_name,
            PortalSummaryReportType.active,
            PortalSummaryReportType.date_modified)
        dbquery = dbquery.filter(PortalSummaryReportType.portal_summary_report_type_id == int(portal_data['portal_summary_report_type_id']))
        if dbquery: 
            dbquery = dbquery.update({
                'active': portal_data['active'], 
                'report_name': portal_data['report_name'], 
                'date_modified': datetime.now()})
            db.session.commit()
        portal_summary_report, success, msg = get_portal_summary_report_type()
        msg = 'User Type updated'
    except Exception as e: 
        print(e)
        msg = e 
    return portal_summary_report, success, msg

def get_portal_summary_report_type(): 
    portal_summary_report = []
    success = False 
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalSummaryReportType.portal_summary_report_type_id, 
            PortalSummaryReportType.report_name,
            PortalSummaryReportType.active,
            PortalSummaryReportType.date_modified)
        portal_summary_report =  [r._asdict() for r in dbquery.all()]
        for report in portal_summary_report: 
            report['date_modified'] = str(report['date_modified'])
        success = True 
        msg = "Report Portal Summary Type retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return portal_summary_report, success, msg