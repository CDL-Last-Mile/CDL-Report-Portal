from report_portal import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(portal_user_id):
    return PortalUsers.query.get(int(portal_user_id))

class PortalUserType(db.Model):
    __tablename__ = "PortalUserType"
    portal_user_type_id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    active = db.Column(db.Integer)

class PortalSummaryReport(db.Model):
    __tablename__ = "PortalSummaryReport"
    portal_summary_report_id = db.Column(db.Integer, primary_key=True)
    report_type_id = db.Column(db.Integer)
    distribution_id = db.Column(db.Integer)
    report_time = db.Column(db.Time)
    report_frequency = db.Column(db.String(255))
    report_url = db.Column(db.String(255))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    active = db.Column(db.Integer)

class PortalSummaryReportType(db.Model):
    __tablename__ = "PortalSummaryReportType"
    portal_summary_report_type_id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    active = db.Column(db.Integer)

class PortalUsers(db.Model, UserMixin):
    __tablename__ = "PortalUsers"
    portal_user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(200))
    hash_password = db.Column(db.String(255))
    portal_user_type_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    active = db.Column(db.Integer)

    def __init__(self):
        pass

    def is_active(self):
        return True
    
    def get_id(self):
           return (self.portal_user_id)

class PortalDistribution(db.Model):
    __tablename__ = "PortalDistribution"
    portal_distribution_id = db.Column(db.Integer, primary_key=True)
    distribution_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    active = db.Column(db.Integer)

class XOrders(db.Model):
    __tablename__ = "xView_Orders"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    PickupTargetFrom = db.Column(db.DateTime)
    DeliveryTargetTo = db.Column(db.DateTime)
    oDate = db.Column(db.DateTime)
    Status = db.Column(db.String(1))
    ServiceID = db.Column(db.Integer)
    ClientID = db.Column(db.Integer)
    RouteID = db.Column(db.Integer)
    DCsegmentID = db.Column(db.Integer)
    DStreet = db.Column(db.String(100))
    DCity = db.Column(db.String(100))
    DState = db.Column(db.String(100))
    DZip = db.Column(db.String(100))
    PODcompletion = db.Column(db.DateTime)
    sPieces =  db.Column(db.Integer)
    GrandTotal = db.Column(db.DECIMAL)
    OrderCharge = db.Column(db.DECIMAL)
    PackageCharge = db.Column(db.DECIMAL)
    WeightCharge = db.Column(db.DECIMAL)
    TotalExtras = db.Column(db.DECIMAL)
    TotalSurcharges = db.Column(db.DECIMAL)


class Orders(db.Model):
    __tablename__ = "Orders"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    PickupTargetFrom = db.Column(db.DateTime)
    DeliveryTargetTo = db.Column(db.DateTime)
    oDate = db.Column(db.DateTime)
    Status = db.Column(db.String(1))
    ServiceID = db.Column(db.Integer)
    ClientID = db.Column(db.Integer)
    RouteID = db.Column(db.Integer)
    DCsegmentID = db.Column(db.Integer)
    DStreet = db.Column(db.String(100))
    DCity = db.Column(db.String(100))
    DState = db.Column(db.String(100))
    DZip = db.Column(db.String(100))
    PODcompletion = db.Column(db.DateTime)
    sPieces =  db.Column(db.Integer)
    GrandTotal = db.Column(db.DECIMAL)
    OrderCharge = db.Column(db.DECIMAL)
    PackageCharge = db.Column(db.DECIMAL)
    WeightCharge = db.Column(db.DECIMAL)
    TotalExtras = db.Column(db.DECIMAL)
    TotalSurcharges = db.Column(db.DECIMAL)
    


class OrderScans(db.Model):
    __tablename__ = "OrderScans"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    aTimeStamp = db.Column(db.DateTime)

class XOrderDrivers(db.Model):
    __tablename__ = "xView_OrderDrivers"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    ArchiveLevel = db.Column(db.Integer, primary_key=True)
    DriverID = db.Column(db.Integer, primary_key=True)
    DrvCommTotal = db.Column(db.DECIMAL)

class OrderDrivers(db.Model):
    __tablename__ = "OrderDrivers"
    OrderTrackingID = db.Column(db.Integer, primary_key=True)
    ArchiveLevel = db.Column(db.Integer, primary_key=True)
    DriverID = db.Column(db.Integer, primary_key=True)
    DrvCommTotal = db.Column(db.DECIMAL)

class Employees(db.Model):
    __tablename__ = "Employees"
    ID = db.Column(db.Integer, primary_key=True)
    DriverNo = db.Column(db.Integer)
    LastName = db.Column(db.String(35))
    FirstName = db.Column(db.String(35))
    TerminalID = db.Column(db.Integer)
    Driver = db.Column(db.String(1))
    Status = db.Column(db.String(1))
    DriverType = db.Column(db.String(1))


class DCSegments(db.Model):
    __tablename__ = "DCsegments"
    DCsegmentID = db.Column(db.Integer, primary_key=True)
    TerminalID = db.Column(db.Integer)
    Name = db.Column(db.String(35))
    sTimeStamp = db.Column(db.DateTime)
    UserID = db.Column(db.Integer)
    Status = db.Column(db.String(1))

class Terminals(db.Model):
    __tablename__ = "Terminals"
    TerminalID = db.Column(db.Integer, primary_key=True)
    TerminalName = db.Column(db.String(500))
    Status = db.Column(db.String(1))

class ClientMaster(db.Model): 
    __tablename__ = "ClientMaster"
    ClientID = db.Column(db.Integer, primary_key=True)
    AccountNo = db.Column(db.String(18))

class SamplePortalOffer(db.Model): 
    __tablename__ = "SamplePortalOffer"
    id = db.Column(db.Integer, primary_key=True)
    offername = db.Column(db.String(250))
    imageUrl = db.Column(db.String(250))
    dateAdded = db.Column(db.String(250))
    offerdescription = db.Column(db.String(250))
    offervalue = db.Column(db.Integer)
    currency = db.Column(db.String(250))
    visitedCount = db.Column(db.Integer)
