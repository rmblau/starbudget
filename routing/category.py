from starlette.routing import Route, Mount
from views import views
from starlette.staticfiles import StaticFiles

static = StaticFiles(directory="static")
routes = [
    Route('/categories', views.categories, methods=["GET", "POST"]),
    Route('/create_category', views.create_category, methods=["GET","POST"]),
    Route("/category_response",
          views.category_response, methods=["POST"]),
    Mount("/static", static, name="static")
]
