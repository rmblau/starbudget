from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from budgeting.user import User

templates = Jinja2Templates(directory='templates')


def google_auth():
    config = Config('.env')
    oauth = OAuth(config)

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile',
            'prompt': 'select_account',
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


async def login(request):
    request.session.clear()
    google = google_auth().create_client('google')
    redirect_uri = request.url_for('auth')
    return await google.authorize_redirect(request, redirect_uri)


async def logout(request):
    request.session.clear()
    request.session['user'] = "Logged_out"
    print(request.session)
    return RedirectResponse(url='/')


async def github_login(request):
    request.session.clear()
    print(request.session.get("user"))
    github = github_auth().github
    redirect_uri = request.url_for('github_auth')
    return await github.authorize_redirect(request, redirect_uri)


async def github_authorize(request):
    token = await github_auth().github.authorize_access_token(request)
    resp = await github_auth().github.get('user', token=token)
    request.session['user'] = resp.json()
    return RedirectResponse(url='/transaction')


async def auth(request):
    if request.session.get("user") == "Logged_out":
        request.session.pop("user", None)
        return RedirectResponse(url='login')
    token = await google_auth().google.authorize_access_token(request)
    session_user = token.get('userinfo')
    if session_user:
        request.session['user'] = session_user
        database_user = User()
        existing_user = await database_user.get_user(session_user['sub'])
        if existing_user:
            return RedirectResponse("/dashboard")

        else:
            print("no user found, redirecting to first_login")
            return RedirectResponse("/first_login")
    else:

        return RedirectResponse(url='/')
