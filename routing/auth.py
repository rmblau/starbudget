from starlette.routing import Route
from budgeting import auth


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
