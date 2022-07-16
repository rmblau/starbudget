from datetime import datetime
from budgeting.budget import Budget
from budgeting.transaction import Transactions
from budgeting.categories import Categories
from budgeting.user import User
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from starlette_core.paginator import Paginator
from views.forms import CreateAccountForm, CreateUserForm, FirstLogin, UpdateCategories, BalanceForm, CreateCategories

templates = Jinja2Templates(directory='templates')


async def homepage(request):
    template = "login.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def index(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context=context)


async def first_login_response(request):
    user = User()
    category = Categories()
    session_user = request.session.get("user")
    data = await request.form()
    if 'sub' in session_user:
        await user.create_balance(session_user['sub'], data['balance'])
        await category.create_category(session_user['sub'], data['categories'])
    if 'id' in session_user:
        await user.create_balance(session_user['id'], data['balance'])
        await category.create_category(session_user['id'], data['category'])
    return RedirectResponse('/success')


async def budget(request):
    user = request.session.get("user")
    print(user)
    if user is not None:
        if 'sub' in user:
            print(user)
            template, context = await render_budget(request, user['sub'])
            return templates.TemplateResponse(template, context=context)
        elif 'id' in user:
            template, context = await render_budget(request, user['id'])
            return templates.TemplateResponse(template, context=context)
    return RedirectResponse("/auth/login")


async def render_budget(request, user_id):
    budget = Budget()
    user = User()
    category = Categories()
    transactions = Transactions()
    transaction = await transactions.get_transaction(user_id=user_id)
    print([t.categories for t in transaction])
    categories = await category.get_user_categories(user_id=user_id)
    balance = await user.get_balance(user_id)
    print(f'categories are {[c.name for c in categories]}')
    sum_of_transacations = await transactions.sum_of_transactions(user_id=user_id)
    paginator = Paginator(transaction, 10)  # Show 10 transactions per page
    page_number = request.query_params.get("page", 1)
    page = paginator.get_page(page_number)
    template = "budget.html"
    context = {"request": request, "paginator": paginator,
               "page": page, "budget": budget, "sum": sum_of_transacations, "categories": [c.name for c in categories], "balance": balance}

    return template, context


async def index(request):
    user = request.session.get("user")
    budget = Budget()
    print(await budget.get_category_id(user['sub']))
    print(user)
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('index.html')
        form = await CreateUserForm.from_formdata(request)
        html = template.render(form=form)
        return HTMLResponse(html)
    elif 'id' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('index.html')
        form = await CreateUserForm.from_formdata(request)
        html = template.render(form=form)
        return HTMLResponse(html)
    else:
        return RedirectResponse("auth/login")


async def success(request):
    template = 'response.html'
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def user_info(request):
    session_user = request.session.get("user")
    user = User()
    print(f'user is {session_user}')
    data = await request.form()
    transaction = Transactions()
    if 'sub' in user:
        await transaction.add_transaction(data['transacation'],
                                          note=data['note'],
                                          user_id=session_user['sub'],
                                          categories=data['categories'])

    elif 'id' in user:
        await transaction.add_transaction(data['transaction'],
                                          note=data['note'],
                                          date_of_transaction=datetime.strptime(
            data['date_of_transaction'], "%Y-%m-%d"),
            user_id=session_user['id'],
            categories=data['categories']
        )
    return RedirectResponse('/success')


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
        form = await UpdateCategories.from_formdata(request)
        context = {"request": request, "categories": [
            c.name for c in categories], "form": form}
        return templates.TemplateResponse(template, context=context)


async def create_category(request):
    categories = Categories()
    user = request.session.get("user")
    data = await request.form()
    print(data)
    if 'sub' in user:
        reponse = await categories.create_category(user['sub'], data['categories'])
        return RedirectResponse('/success')
    return RedirectResponse("/auth/login")


async def category_response(request):
    category = Categories()

    user = request.session.get("user")
    print(f'request is {await request.form()}')
    button_click = request.get("data", False)
    print(f'button clicked is {button_click}')
    print(user)
    data = await request.form()

    if 'sub' in user:
        if 'btnrenameCategory' in data:
            print('rename found')
        else:
            print("Not found")
        user_categories = [c.name for c in await category.get_user_categories(user['sub'])]
        print(f'data is {data}')
        print(user_categories)
        response = await category.update_category_name(data['newname'], data['oldname'], user['sub'])
        return RedirectResponse('/categories')
    return RedirectResponse('/auth/login')


async def create_category_form(request):
    session_user = request.session.get("user")
    data = await request.form()
    template = "category.html"
    form = await CreateCategories.from_formdata(request)
    context = {"request": request, "form": form}
    return templates.TemplateResponse(template, context)


async def balance(request):
    user = request.session.get("user")
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('balance.html')
        form = await BalanceForm.from_formdata(request)
        if form.validate_on_submit():
            html = template.render(form=form)
            return HTMLResponse(html)


async def balance_response(request):
    user = User()
    session_user = request.session.get("user")
    data = await request.form()
    if 'sub' in session_user:
        await user.create_balance(session_user['sub'], data['balance'])

        return RedirectResponse('/success')


async def dashboard(request):
    session_user = request.session.get("user")
    if session_user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('dashboard.html')
        user_balance = User()
        transactions = Transactions()
        category = Categories()
        user = request.session.get("user")
        form = await CreateAccountForm.from_formdata(request)
        categories = await category.get_user_categories(user['sub'])
        if categories is not None:
            form.categories.choices = [c.name for c in categories]
        else:
            form.categories.choices = ""
        balance = await user_balance.get_balance(user['sub'])
        total_expenses = await transactions.sum_of_transactions(user['sub'])
        last_five_transaction_amounts = [t.amount for t in await transactions.last_five_transactions(user['sub'])]
        last_five_names = [t.note for t in await transactions.last_five_transactions(user['sub'])]
        last_five_categories = [t.categories for t in await transactions.last_five_transactions(user['sub'])]
        context = {"request": request, "categories": categories,
                   "balance": balance, "last_five": zip(last_five_names, last_five_transaction_amounts, last_five_categories),
                   "expenses": total_expenses, "form": form}
        return templates.TemplateResponse(template, context=context)
    else:
        return RedirectResponse("auth/login")


async def first_login(request):
    template = 'first_login.html'
    form = await FirstLogin.from_formdata(request)
    if form.validate_on_submit():
        context = {"request": request, "form": form}
        return templates.TemplateResponse(template, context)


async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)

exception_handlers = {
    404: not_found,
    500: server_error
}
