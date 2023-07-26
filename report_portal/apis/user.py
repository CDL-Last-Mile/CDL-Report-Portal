from report_portal.models import PortalUsers, PortalUserType, Terminals, Employees, DCSegments
from sqlalchemy import Date
from report_portal.config import config
from datetime import datetime
from report_portal import db
import uuid

def add_portal_user_type(user_type):
    user_types = []
    success = False 
    msg = ''
    try:
        if user_type:
            new_user_type = PortalUserType()
            new_user_type.user_type = str(user_type)
            new_user_type.active = 1
            db.session.add(new_user_type)
            db.session.commit()
            
            user_types, success, msg = get_portal_user_types()
            msg = "User Type added"
    except Exception as e: 
        print(e)
        msg = e
    return user_types, success, msg

def get_portal_user_types(): 
    user_types = []
    success = False
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalUserType.portal_user_type_id, 
            PortalUserType.user_type,
            PortalUserType.active)
        user_types =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = "User Types retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return user_types, success, msg

def update_portal_user_type(portal_data) :
    user_types = []
    success = False 
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalUserType.active, 
            PortalUserType.user_type,
            PortalUserType.portal_user_type_id)
        dbquery = dbquery.filter(PortalUserType.portal_user_type_id == portal_data['portal_user_type_id'])
        dbquery = dbquery.update({'user_type': portal_data['user_type'], 'active': portal_data['active']})
        db.session.commit()
        user_types, success, msg = get_portal_user_types()
        msg = 'User Type updated'
    except Exception as e: 
        print(e)
        msg = e 
    return user_types, success, msg



def register_user(firstname, lastname, email, password):
    success = False 
    user = []
    msg = ''
    try:
        dbquery = db.session.query(PortalUsers.email)
        dbquery = dbquery.filter(PortalUsers.email == email).first()
        if dbquery is not None: 
            success = False
            msg = 'Email already exists.'
        else:
            new_user = PortalUsers()
            new_user.first_name = firstname
            new_user.active = 1
            new_user.portal_user_type_id = 1
            new_user.last_name = lastname
            new_user.hash_password = password
            new_user.email = email
            new_user.date_created = datetime.now()
            db.session.add(new_user)
            db.session.commit()
            success = True
            user, success, msg = get_portal_user_by_id(new_user.portal_user_id)
            user[0]['auth_token'] = uuid.uuid4().hex[:24]
    except Exception as e: 
        print(e)
        msg = e
    return user, success, msg

def get_portal_users(): 
    users = []
    success = False
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalUsers.portal_user_id,
            PortalUsers.first_name,
            PortalUsers.last_name,
            PortalUsers.email,
            PortalUsers.active,
            PortalUsers.portal_user_type_id)
        dbquery = dbquery.filter(PortalUsers.active == 1)
        users =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = "Users retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return users, success, msg

def get_portal_user_by_id(portal_user_id): 
    user = []
    success = False
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalUsers.portal_user_id,
            PortalUsers.first_name,
            PortalUsers.last_name,
            PortalUsers.active,
            PortalUsers.email,
            PortalUsers.portal_user_type_id)
        dbquery = dbquery.filter(PortalUsers.portal_user_id == portal_user_id)
        user =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = "User data retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return user, success, msg

def update_portal_user_by_id(portal_data): 
    user = []
    success = False
    msg = ''
    try: 
        dbquery = db.session.query(
            PortalUsers.first_name,
            PortalUsers.last_name,
            PortalUsers.email,
            PortalUsers.active,
            PortalUsers.portal_user_type_id)
        dbquery = dbquery.filter(PortalUsers.portal_user_id == portal_data['portal_user_id'])
        dbquery = dbquery.update({
            'email': portal_data['email'], 
            'active': portal_data['active'],
            'first_name': portal_data['first_name'],
            'last_name': portal_data['last_name'],
            'portal_user_type_id': portal_data['portal_user_type_id']})
        db.session.commit()
        user, success, msg = get_portal_users()
        success = True 
        msg = "User data retrieved successfully "
    except Exception as e: 
        print(e)
        msg = e 
    return user, success, msg


def get_terminals():
    terminals = []
    success = False 
    try: 
        dbquery = db.session.query(Terminals.TerminalID.label('terminal_id'), Terminals.TerminalName.label('terminal_name'))
        dbquery = dbquery.filter(Terminals.Status == 'A')
        terminals =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = 'Terminals loaded'
    except Exception as e: 
        msg = str(e) 
    return terminals, success, msg

def get_dc_segments():
    segments = []
    success = False 
    try: 
        dbquery = db.session.query(DCSegments.TerminalID.label('terminal_id'), DCSegments.Name.label('terminal_name'), DCSegments.DCsegmentID.label('dc_segment_id'))
        dbquery = dbquery.filter(DCSegments.Status == 'A')
        # dbquery = dbquery.filter(DCSegments.DCsegmentID.in_(config.DC_SEGMENTS))
        segments =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = 'DC Segments loaded'
    except Exception as e: 
        msg = str(e) 
    return segments, success, msg

def get_driver_dc():
    terminals = []
    success = False 
    try: 
        dbquery = db.session.query(Terminals.TerminalID.label('terminal_id'), Terminals.TerminalName.label('terminal_name'))
        # dbquery = dbquery.filter(Terminals.TerminalID.in_(config.DRIVER_DC))
        terminals =  [r._asdict() for r in dbquery.all()]
        success = True 
        msg = 'Terminals loaded'
    except Exception as e: 
        msg = str(e) 
    return terminals, success, msg

def get_driver_type():
    driver_types = []
    success = False 
    try: 
        # dbquery = db.session.query(Employees.DriverType)
        # driver_types = [r._asdict() for r in dbquery.all()]
        driver_types = [{'DriverType': 'C'}, {'DriverType': 'E'}]
        success = True
        msg = 'Driver Types loaded successful'
    except Exception as e:
        print(e)
        msg = str(e)
        
    return driver_types, success, msg

