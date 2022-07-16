from starlette.routing import Route
from views import views, transaction_view


routes = [
    # Route("/", views.homepage, name="home", methods=["GET"]),
    # Route("/index", views.index, name="index", methods=["GET"]),
    # Route("/budget", views.budget, name="budget", methods=["GET", "POST"]),
    # Route("/transaction", transaction_view.transaction_add_form,
    #      name="transaction", methods=["GET", "POST"]),
    Route("/success", views.success, name="success", methods=["GET", "POST"]),
    # Route("/response", transaction_view.add_transaction_response,
    #      name="response", methods=["POST"]),
    # Route('/create_user', views.user_info, methods=["POST"]),
    # Route('/categories', views.categories, methods=["GET", "POST"]),
    # Route('/create_category', views.create_category, methods=["POST"]),
    # Route("/category_response", views.category_response,
    #      methods=["GET", "POST"]),
    # Route('/balance', views.balance, methods=["GET", "POST"]),
    # Route('/update_balance', views.balance_response, methods=['POST']),
    # Route('/dashboard', views.dashboard, methods=["GET"]),
    # Route('/first_login', views.first_login, methods=["GET", "POST"]),
    # Route('/first_login_response',
    #      views.first_login_response, methods = ["GET", "POST"]),
]
