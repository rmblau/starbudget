from starlette.routing import Route, Mount
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from views import views, transaction_view
from budgeting import auth
from budgeting.base import create_table


routes = [
    Route("/login", auth.login,
          name="login", methods=["GET", "POST"]),
    Route("/verify", auth.auth,
          name="auth", methods=["GET"]),
    Route("/github_login", auth.github_login,
          name="github_login", methods=["GET", "POST"]),
    Route("/github_auth", auth.github_authorize,
          name="github_auth", methods=["GET", "POST"]),
    Route("/logout", auth.logout,
          name="logout", methods=["GET", "POST"]),
]
