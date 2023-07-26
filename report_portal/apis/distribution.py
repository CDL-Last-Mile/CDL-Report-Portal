from report_portal.models import PortalDistribution
from report_portal import db
from datetime import datetime

def get_portal_distribution(): 
    portal_distribution = []
    success = False
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalDistribution.portal_distribution_id, 
            PortalDistribution.distribution_name, 
            PortalDistribution.email, 
            PortalDistribution.active)
        # dbquery = dbquery.filter(PortalDistribution.active == 1)
        portal_distribution =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = "Distributions retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return portal_distribution, success, msg

def add_portal_distribution(portal_data):
    portal_distribution = []
    success = False 
    msg = ''
    try:
        new_portal_distribution = PortalDistribution()
        new_portal_distribution.email = portal_data['email']
        new_portal_distribution.active = 1
        new_portal_distribution.distribution_name = portal_data['distribution_name']
        new_portal_distribution.date_created = datetime.now()
        db.session.add(new_portal_distribution)
        db.session.commit()
        portal_distribution, success, msg = get_portal_distribution()
        msg = 'Distribution added'
    except Exception as e: 
        print(e)
        msg = e
    return portal_distribution, success, msg 


def update_portal_distribution(portal_data):
    portal_distribution = []
    success = False 
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalDistribution.portal_distribution_id,
            PortalDistribution.distribution_name,
            PortalDistribution.email,
            PortalDistribution.active)
        dbquery = dbquery.filter(PortalDistribution.portal_distribution_id == portal_data['portal_distribution_id'])
        if dbquery:
            dbquery.update({
                'distribution_name': portal_data['distribution_name'], 
                'email': portal_data['email'], 
                'active': portal_data['active']
                })
        db.session.commit()
        portal_distribution, success, msg = get_portal_distribution()
        msg = 'User Type updated'
    except Exception as e: 
        print(e)
        msg = e 
    return portal_distribution, success, msg