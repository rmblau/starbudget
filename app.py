
from starlette.routing import Route, Mount
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
import uvicorn
from views import views, transaction_view
from budgeting.base import create_table
from routing import auth, routes, category

static = StaticFiles(directory="static")
routes = [
    Route("/", views.homepage, name="home", methods=["GET"]),
    Mount('/auth', routes=auth.routes),
    Route("/index", views.index, name="index", methods=["GET"]),
    Route("/budget", views.budget, name="budget", methods=["GET", "POST"]),
    Route("/transaction", transaction_view.transaction_add_form,
          name="transaction", methods=["GET", "POST"]),
    Route("/update_or_delete_transaction", views.update_or_delete_transaction,
          methods=['GET', 'POST']),
    Route("/success", views.success, name="success", methods=["GET", "POST"]),
    Route("/response", transaction_view.add_transaction_response,
          name="response", methods=["POST"]),
    Route('/create_user', views.user_info, methods=["POST"]),
    Route('/categories', views.categories, methods=["GET", "POST"]),
    Route('/create_category', views.create_category, methods=["GET", "POST"]),
    Route("/category_response", views.category_response, methods=["POST"]),
    Route("/delete_category", views.delete_category, methods=["POST"]),
    Route("/category_create", views.create_category_form,
          methods=["GET", "POST"]),
    Route('/balance', views.balance, methods=["GET", "POST"]),
    Route('/update_balance', views.balance_response, methods=['POST']),
    Route('/dashboard', views.dashboard, methods=["GET", "POST"]),
    Route('/first_login', views.first_login, methods=["GET", "POST"]),
    Route('/first_login_response',
          views.first_login_response, methods=["GET", "POST"]),
    Route('/income', views.income, methods=["GET", "POST"]),
    Route('/income_response', views.income_response, methods=["GET", "POST"]),
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
app.add_middleware(SessionMiddleware, secret_key="!secret", max_age=None)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,
                ssl_keyfile="./localhost+3-key.pem", ssl_certfile="./localhost+3.pem")
