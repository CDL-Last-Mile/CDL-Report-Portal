from flask import render_template, request, Blueprint, redirect, url_for, make_response
from datetime import date, datetime
from sqlalchemy import Date
from report_portal import mail, db, bcrypt
from report_portal.config import config
from report_portal.utils import json_return
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_cors import cross_origin
from report_portal.apis.user import (
    add_portal_user_type,
    update_portal_user_type,
    get_portal_user_types,
    register_user,
    get_portal_users,
    get_portal_user_by_id,
    update_portal_user_by_id,
    get_terminals,
    get_driver_type,
    get_dc_segments,
    get_driver_dc
)
from report_portal.apis.distribution import (
    add_portal_distribution,
    update_portal_distribution,
    get_portal_distribution
)

from report_portal.models import PortalUsers
import uuid

main = Blueprint('main', __name__)


# Define decorator function
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,content-type,authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response


# Apply decorator function to all routes
@main.after_request
def after_request(response):
    return add_cors_headers(response)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/user-type/", methods=['GET'])
def get_user_type_route():
    user_types, success, msg = get_portal_user_types()
    return json_return(user_types, success, msg)


@main.route("/user-type/add/", methods=['POST'])
def add_user_type_route():
    input_data = request.get_json()
    user_types, success, msg = add_portal_user_type(input_data['user_type'])
    return json_return(user_types, success, msg)


@main.route("/user-type/update/", methods=['POST'])
def edit_user_type_route():
    input_data = request.get_json()
    dc_segment = input_data['dc_segment']
    aging = input_data['dc_segment']
    threshold = input_data['dc_segment']
    user_types, success, msg = update_portal_user_type(input_data['portal_data'])
    return json_return(user_types, success, msg)


@main.route("/distribution/", methods=['GET'])
def get_portal_distribution_route():
    portal_distributions, success, msg = get_portal_distribution()
    return json_return(portal_distributions, success, msg)


@main.route("/distribution/add/", methods=['POST'])
def add_portal_distribution_route():
    input_data = request.get_json()
    portal_distributions, success, msg = add_portal_distribution(input_data['portal_data'])
    return make_response(json_return(portal_distributions, success, msg))


@main.route("/distribution/update/", methods=['POST'])
def update_portal_distribution_route():
    input_data = request.get_json()
    portal_data = input_data['portal_data']
    portal_distributions, success, msg = update_portal_distribution(portal_data)
    return make_response(json_return(portal_distributions, success, msg))


@main.route("/register/", methods=['POST'])
def register_user_route():
    if current_user.is_authenticated:
        return {'data': {'success': False, 'msg': 'User is already registered. Logout to register a new account.'}}
    hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
    firstname = request.form.get('first_name')
    lastname = request.form.get('last_name')
    email = request.form.get('email')
    user, success, msg = register_user(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
    return json_return(user, success, msg)


@main.route("/users/", methods=['GET'])
def get_users_route():
    users, success, msg = get_portal_users()
    return json_return(users, success, msg)


@main.route("/user/", methods=['GET'])
def get_user_by_id_route():
    input_data = request.get_json()
    portal_data = input_data['portal_data']
    users, success, msg = get_portal_user_by_id(portal_data['portal_user_id'])
    return json_return(users, success, msg)


@main.route("/user/update/", methods=['POST'])
def update_user_by_id_route():
    input_data = request.get_json()
    portal_data = input_data['portal_data']
    users, success, msg = update_portal_user_by_id(portal_data)
    return json_return(users, success, msg)


@main.route("/login/", methods=['POST'])
def login():
    if current_user.is_authenticated:
        return {'data': {'success': True, 'msg': 'user already logged in'}}
    user = PortalUsers.query.filter_by(email=request.form.get('email')).first()
    if user and bcrypt.check_password_hash(user.hash_password, request.form.get('password')):
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        else:
            return {
                'data': {'success': True, 'msg': 'User Logged In Successfully', 'auth_token': uuid.uuid4().hex[:24]}}
        # return redirect(next_page) if next_page else redirect(url_for('home'))        
    return {'data': {'success': False, 'msg': 'Login not successful'}}


@main.route("/logout/", methods=['PATCH'])
def logout():
    logout_user()
    return {'data': {'success': True, 'msg': 'User Logged Out Successfully', 'auth_token': None}}


@main.route("/terminals/", methods=['GET'])
def terminals_rte():
    terminals, success, msg = get_terminals()
    return json_return(terminals, success, msg)


@main.route("/driver-dc/", methods=['GET'])
def get_driver_dc_rte():
    terminals, success, msg = get_driver_dc()
    return json_return(terminals, success, msg)


@main.route("/segments/", methods=['GET'])
def get_dc_segmentc_rte():
    dc_segments, success, msg = get_dc_segments()
    return json_return(dc_segments, success, msg)


@main.route("/driver-types/", methods=['GET'])
def driver_types_rte():
    drivers, success, msg = get_driver_type()
    return json_return(drivers, success, msg)
