from datetime import datetime
from budgeting.budget import Budget
from budgeting.base import create_table
from authlib.integrations.starlette_client import OAuth
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from starlette.config import Config
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.authentication import requires
from starlette_wtf import StarletteForm
from starlette_core.paginator import Paginator
from wtforms import TextField, DateField, SelectField, DecimalField
from wtforms.validators import DataRequired
from budgeting.base import create_table
templates = Jinja2Templates(directory='templates')


def google_auth():
    config = Config('.env')
    oauth = OAuth(config)

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        },
        client_id=config.get('GOOGLE_CLIENT_ID'),
        client_secret=config.get('GOOGLE_CLIENT_SECRET')
    )

    return oauth


def github_auth():
    config = Config('.env')
    github_oauth = OAuth(config)
    github_oauth.register(
        name='github',
        client_id=config.get("GITHUB_CLIENT_ID"),
        client_secret=config.get('GITHUB_CLIENT_SECRET'),
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )
    print(github_oauth._clients)
    return github_oauth


oauth = google_auth()
github_oauth = github_auth()


class CreateAccountForm(StarletteForm):
    transaction = TextField(
        'Transaction amount',
        validators=[
            DataRequired('Amount')
        ]
    )
    note = TextField(
        'Transaction notes',
        validators=[DataRequired('Note')]
    )
    date_of_transaction = DateField('DatePicker',
                                    validators=[DataRequired('Date')],
                                    format="%Y-%m-%d"
                                    )
    categories = SelectField('SelectField', validators=[
                             DataRequired('categories')])


class CreateUserForm(StarletteForm):
    name = TextField(
        'Name of user',
        validators=[
            DataRequired('Name')
        ]
    )
    categories = TextField(
        'Category',
        validators=[DataRequired('Note')]
    )
    balance = DecimalField('Balance', validators=[DataRequired("Balance")])


async def homepage(request):
    template = "login.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def login(request):
    google = oauth.create_client('google')
    redirect_uri = request.url_for('auth')
    return await google.authorize_redirect(request, redirect_uri)


async def github_login(request):
    github = github_oauth.github
    redirect_uri = request.url_for('github_auth')
    return await github.authorize_redirect(request, redirect_uri)


async def github_authorize(request):
    token = await github_oauth.github.authorize_access_token(request)
    resp = await github_oauth.github.get('user', token=token)
    request.session['user'] = resp.json()
    return RedirectResponse(url='/transaction')


async def auth(request):
    token = await oauth.google.authorize_access_token(request)
    print(f'token is :{token["id_token"]}')
    user = token.get('userinfo')
    if user:
        request.session['user'] = user
        return RedirectResponse(url='/transaction', headers={"Authorization": f"Bearer {token['id_token']}"})
    else:

        return RedirectResponse(url='/')


async def index(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context=context)


async def logout(request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


async def budget(request):
    user = request.session.get("user")
    budget = Budget()
    print(user)
    if user is not None:
        if 'sub' in user:
            print(user)
            template, context = await render_budget(request, user['sub'])
            return templates.TemplateResponse(template, context=context)
        elif 'id' in user:
            template, context = await render_budget(request, user['id'])
            return templates.TemplateResponse(template, context=context)
    return JSONResponse({"error": "not authed"})


async def render_budget(request, user):
    budget = Budget()
    transaction = await budget.get_transaction(user_id=user)
    categories = await budget.get_user_categories(user_id=user)
    sum_of_transacations = await budget.sum_of_transactions(user_id=user)
    paginator = Paginator(transaction, 10)  # Show 10 transactions per page
    page_number = request.query_params.get("page", 1)
    page = paginator.get_page(page_number)
    template = "budget.html"
    context = {"request": request, "paginator": paginator,
               "page": page, "budget": budget, "sum": sum_of_transacations, "categories": categories}

    return template, context


async def transaction_add(request):
    user = request.session.get("user")
    budget = Budget()
    print(user)
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('add_transaction.html')
        categories = await budget.get_user_categories(user['sub'])
        form = await CreateAccountForm.from_formdata(request)
        if categories is not None:
            form.categories.choices = [c.name for c in categories]
        else:
            form.categories.choices = "Test"
        html = template.render(form=form)
        return HTMLResponse(html)
    elif 'id' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('add_transaction.html')
        form = await CreateAccountForm.from_formdata(request)
        html = template.render(form=form)
        return HTMLResponse(html)
    else:
        return RedirectResponse("/login")


async def index(request):
    user = request.session.get("user")
    budget = Budget()
    print(user)
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('index.html')
        form = await CreateUserForm.from_formdata(request)
        html = template.render(form=form)
        return HTMLResponse(html)
    elif 'id' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('index.html')
        form = await CreateUserForm.from_formdata(request)
        html = template.render(form=form)
        return HTMLResponse(html)
    else:
        return RedirectResponse("/login")


async def success(request):
    template = 'response.html'
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def add_transaction(request):
    user = request.session.get("user")
    print(user)
    data = await request.form()
    budget = Budget()
    if 'sub' in user:
        await budget.add_transaction(data['transaction'],
                                     note=data['note'],
                                     date_of_transaction=datetime.strptime(
                                         data['date_of_transaction'], "%Y-%m-%d"),
                                     user_id=user['sub'],
                                     categories=None)

    elif 'id' in user:
        await budget.add_transaction(data['transaction'],
                                     note=data['note'],
                                     date_of_transaction=datetime.strptime(
                                         data['date_of_transaction'], "%Y-%m-%d"),
                                     user_id=user['id'],
                                     categories=None
                                     )
    return RedirectResponse('/success')


async def user_info(request):
    user = request.session.get("user")
    print(user)
    data = await request.form()
    budget = Budget()
    if 'sub' in user:
        await budget.create_user(data['name'],
                                 user_id=user['sub'],
                                 bank_balance=data['balance'],
                                 categories=data['categories'])

    elif 'id' in user:
        await budget.add_transaction(data['transaction'],
                                     note=data['note'],
                                     date_of_transaction=datetime.strptime(
                                         data['date_of_transaction'], "%Y-%m-%d"),
                                     user_id=user['id'],
                                     categories=data['categories']
                                     )
    return RedirectResponse('/success')


async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)

exception_handlers = {
    404: not_found,
    500: server_error
}
