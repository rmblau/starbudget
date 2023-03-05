from starlette.routing import Route, Mount
from starlette.middleware.sessions import SessionMiddleware
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import uvicorn
from views import views, transaction_view, category_views
from budgeting.base import create_table
from routing import auth
import string
import secrets
from starlette.config import Config
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration

alphabet = string.ascii_letters + string.digits
static = StaticFiles(directory="static")
routes = [
    Route("/", views.homepage, name="home", methods=["GET"]),
    Mount('/auth', routes=auth.routes),
    Route("/index", views.index, name="index", methods=["GET"]),
    Route("/transactions", views.budget, name="transactions", methods=["GET", "POST"]),
    Route("/transaction", transaction_view.transaction_add_form,
          name="transaction", methods=["GET", "POST"]),
    Route("/update_or_delete_transaction", transaction_view.update_or_delete_transaction,
          methods=['GET', 'POST']),
    Route("/response", transaction_view.add_transaction_response,
          name="response", methods=["POST"]),
    Route('/categories', category_views.categories, methods=["GET", "POST"]),
    Route('/create_category', category_views.create_category, methods=["GET", "POST"]),
    Route("/category_response", category_views.category_response, methods=["POST", "GET"]),
    Route("/update_category_balance/{category:str}", category_views.update_category_balance_request, methods=['POST']),
    Route("/delete_category", category_views.delete_category, methods=["POST"]),
    Route("/category_detail/{category:str}", category_views.category_detail, methods=["GET", "POST"]),
    Route("/category_create", category_views.create_category_form,
          methods=["GET", "POST"]),
    Route('/balance', views.balance, methods=["GET", "POST"]),
    Route('/update_balance', views.balance_response, methods=['POST']),
    Route('/dashboard', views.dashboard, methods=["GET", "POST"]),
    Route('/first_login', views.first_login, methods=["GET", "POST"]),
    Route('/first_login_response',
          views.first_login_response, methods=["GET", "POST"]),
    Route('/income', views.income, methods=["GET", "POST"]),
    Route("/income_add_response", transaction_view.income_add_response, methods=["POST"]),
    Route('/reports', views.reports, methods=["GET"]),
    Mount("/static", static, name="static")
]


async def startup():
    table = await create_table()
    return table

config = Config(".env")
sentry_sdk.init(
    dsn=config.get("SENTRY_DSN"),
    integrations=[StarletteIntegration(transaction_style="url")],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.5
)
app = Starlette(debug=False,
                routes=routes,
                exception_handlers=views.exception_handlers,
                on_startup=[startup],
                )
app.add_middleware(SessionMiddleware, secret_key=''.join(
    secrets.choice(alphabet) for i in range(30)), max_age=None)

if __name__ == "__main__":
    if config.get("ENVIRONMENT") == "LOCAL":
        uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="./localhost+3-key.pem",
                    ssl_certfile="./localhost+3.pem")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000,
                    ssl_keyfile="/etc/starbudget/live/starbudget.rmblau.com/privkey.pem",
                    ssl_certfile="/etc/starbudget/live/starbudget.rmblau.com/fullchain.pem", proxy_headers=True)
