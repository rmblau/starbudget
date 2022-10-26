from jinja2 import FileSystemLoader, Environment
from starlette.templating import Jinja2Templates

from budgeting.categories import Categories
from views.forms import UpdateCategories
templates = Jinja2Templates(directory='templates')

async def categories(request):
    user = request.session.get("user")
    category = Categories()
    categories = await category.get_user_categories(user['sub'])
    template = "categories.html"
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('categories.html')
        categories = await category.get_user_categories(user['sub'])
        print(categories)
        form = await UpdateCategories.from_formdata(request)
        context = {"request": request, "categories":
                   [c.name for c in categories], "form": form}
        return templates.TemplateResponse(template, context=context)
