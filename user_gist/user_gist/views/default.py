from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound

from ..models import MyModel


@view_config(route_name="register", renderer="../templates/register.jinja2")
def register_view(request):
    if request.method == "POST":
        new_username = request.POST["username"]
        new_password = request.POST["password"]
        new_fname = request.POST["fname"]
        new_lname = request.POST["lname"]
        new_email = request.POST["email"]
        new_fav_food = request.POST["fave_food"]
        new_model = MyModel(username=new_username, password=new_password, fname=new_fname, lname=new_lname, email=new_email, fave_food=new_fav_food)

        request.dbsession.add(new_model)

        return {"data": {"name": "We made a new model!"}}

    return {"data": {"name": "A New Form"}}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if username in request.dbsession.query(MyModel) and password == request.dbsession.query(MyModel)[password]:
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url('home'),
                headers=auth_head
            )
    return {}


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {}


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    model = request.dbsession.query(MyModel)
    model_profile = model.filter(MyModel.username == request.matchdict['username']).first()
    return {'model_list': model_profile}


@view_config(route_name='logout')
def logout_view(request):
    auth_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=auth_head)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_user_gist_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
