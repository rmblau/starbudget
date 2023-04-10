from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from budgeting.user import get_user_id

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
    return github_oauth


async def login(request):
    request.session.clear()
    google = google_auth().create_client('google')
    redirect_uri = request.url_for('auth')
    return await google.authorize_redirect(request, redirect_uri)


async def logout(request):
    request.session.clear()
    request.session['user'] = "Logged_out"
    return RedirectResponse(url='/')


async def github_login(request):
    request.session.clear()
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
        existing_user = await get_user_id(session_user['sub'])
        if existing_user:
            return RedirectResponse("/dashboard")

        else:
            return RedirectResponse("/first_login")
    else:

        return RedirectResponse(url='/')
