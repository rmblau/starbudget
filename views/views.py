from datetime import datetime

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates
from starlette_core.paginator import Paginator

from budgeting.categories import Categories
from budgeting.transaction import (
    last_five_transactions, 
    get_transaction,
    sum_of_transactions
    )

from budgeting.user import (
                            get_balance,
                            create_balance,
                            update_user,
                            update_first_login,
                            create_user,
                            get_first_login, sum_of_income
                            )

from views.forms import CreateUserForm, FirstLogin, IncomeForm, BalanceForm, TransactionForm

templates = Jinja2Templates(directory='templates')


async def homepage(request):
    template = "login.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)

async def first_login_response(request):
    category = Categories()
    session_user = request.session.get("user")

    data = await request.form()
    if 'sub' in session_user:
        first_login = get_first_login(session_user['sub'])
        if first_login:
            print(session_user['sub'])
            await create_user(name=session_user['name'], user_id=session_user['sub'], categories=f'{"Uncategorized"}~{session_user["sub"]}', income=0.0, bank_balance=0.0, hidden=True)
            await category.create_category(session_user['sub'], f"{data['categories']}", balance=data['category_balance'])
            await update_first_login(session_user['sub'])
        else:
            await update_user(user_id=session_user['sub'], categories="Uncategorized", bank_balance=0.0)
       # await category.create_category(session_user['sub'], f"{data['categories']}~{session_user['sub']}")
        await create_balance(session_user['sub'], (float(data['balance']) - float(data['category_balance'])))

    if 'id' in session_user:
        first_login = await get_first_login(session_user['id'])
        if first_login:
            await create_user(name=session_user['name'], user_id=session_user['id'], categories="Uncategorized", bank_balance=0.0)
            await update_first_login(session_user['id'])
        else:
            await update_user(user_id=session_user['id'], categories="Uncategorized", bank_balance=0.0)
        await create_balance(session_user['id'], data['balance'])
        await category.create_category(session_user['id'], data['category'])
    return RedirectResponse('/dashboard')


async def budget(request):
    user = request.session.get("user")
    print(user)
    data = await request.form()
    print(data)
    if user is not None:
        if 'sub' in user:
            template, context = await render_budget(request, user['sub'])
            return templates.TemplateResponse(template, context=context)
        elif 'id' in user:
            template, context = await render_budget(request, user['id'])
            return templates.TemplateResponse(template, context=context)
    elif user is None:
        return RedirectResponse("/auth/login")


async def render_budget(request, user_id):
    category = Categories()
    transaction = await get_transaction(user_id)
    categories = await category.get_all_user_categories(user_id=user_id)
    print(f'categories are {[c.name for c in categories]}')
    income = await sum_of_income(user_id)
    balance = await get_balance(user_id)
    total_expenses = await sum_of_transactions(user_id)
    sum_of_transacations = await sum_of_transactions(user_id)
    # Show 10 transactions per page
    paginator = Paginator(transaction, 10)
    page_number = request.query_params.get("page", 1)
    page = paginator.get_page(page_number)
    template = "transactions.html"
    context = {"request": request, "paginator": paginator,
               "page": page, "budget": budget, "sum": sum_of_transacations,
               "categories": [c.name for c in categories],
               "balance": balance, "expenses": total_expenses, "income": income
               }

    return template, context


async def index(request):
    user = request.session.get("user")
    print(await budget.get_category_id(user['sub']))
    print(user)
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('index.html')
        form = await CreateUserForm.from_formdata(request)
        print(f'form categories are {form.categories}')
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


async def income(request):
    session_user = request.session.get("user")
    if 'sub' in session_user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('income.html')
        form = await IncomeForm.from_formdata(request)
        if form.validate_on_submit():
            html = template.render(form=form)
            return HTMLResponse(html)
    return RedirectResponse('/')


async def balance_response(request):
    session_user = request.session.get("user")
    data = await request.form()
    if 'sub' in session_user:
        await create_balance(session_user['sub'], data['balance'])

        return RedirectResponse('/success')

async def dashboard(request):
    session_user = request.session.get("user")
    if session_user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('dashboard.html')
        category = Categories()
        print(await category.get_category_transactions(f'Uncategorized~{session_user["sub"]}', session_user['sub']))
        form = await TransactionForm.from_formdata(request)
        income_form = await IncomeForm.from_formdata(request)
        categories = await category.get_all_user_categories(session_user['sub'])
        if categories is not None:
            form.categories.choices = [
                c.name.split('~')[0] for c in categories]
        else:
            form.categories.choices = ""
        income = await sum_of_income(session_user['sub'])
        balance = await get_balance(session_user['sub'])
        low_balance = False
        if balance < 10:
            low_balance = True
        total_expenses = await sum_of_transactions(session_user['sub'])
        recipient, amount, description, category_stripped = await last_five_transactions(session_user['sub'])
        context = {"request": request, "categories": [c.name for c in categories], "income": income,
                   "balance": balance, "last_five": zip(recipient, amount, description, category_stripped),
                   "expenses": total_expenses, "form": form, "income_form": income_form, "low_balance": low_balance}
        return templates.TemplateResponse(template, context=context)
    else:
        return RedirectResponse("auth/login")

async def reports(request):
    stars = [135850, 52122, 148825, 16939, 9763]
    template = "reports.html"
    context = {"request": request, "stars": stars}
    return templates.TemplateResponse(template, context)

async def first_login(request):
    template = 'first_login.html'
    form = await FirstLogin.from_formdata(request)
    await form.validate_on_submit()
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
