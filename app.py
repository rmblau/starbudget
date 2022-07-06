
from starlette.routing import Route, Mount
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from views import views, test
from budgeting.base import create_table

static = StaticFiles(directory="static")
routes = [
    Route("/", views.homepage, name="home", methods=["GET"]),
    Route("/login", views.login,
          name="login", methods=["GET", "POST"]),
    Route("/auth", views.auth,
          name="auth", methods=["GET"]),
    Route("/github_login", views.github_login,
          name="github_login", methods=["GET", "POST"]),
    Route("/github_auth", views.github_authorize,
          name="github_auth", methods=["GET", "POST"]),
    Route("/index", views.index, name="index", methods=["GET"]),
    Route("/logout", views.logout, name="logout", methods=["GET", "POST"]),
    Route("/budget", views.budget, name="budget", methods=["GET", "POST"]),
    Route("/transaction", views.transaction_add,
          name="transaction", methods=["GET", "POST"]),
    Route("/success", views.success, name="success", methods=["GET", "POST"]),
    Route("/response", views.add_transaction,
          name="response", methods=["POST"]),
    Route("/get_transactions", test.get_transactions, methods=["GET"]),
    Route('/create_user', views.user_info, methods=["POST"]),
    Mount("/static", static, name="static")
]


async def startup():
    table = await create_table()
    return table
app = Starlette(debug=True,
                routes=routes,
                exception_handlers=views.exception_handlers,
                on_startup=[startup],
                )
app.add_middleware(SessionMiddleware, secret_key="!secret")
