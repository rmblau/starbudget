from datetime import datetime
from budgeting.transaction import Transactions
from budgeting.categories import Categories
from budgeting.user import User
from budgeting.base import create_table
from authlib.integrations.starlette_client import OAuth
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from starlette.config import Config
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from starlette_core.paginator import Paginator
from budgeting.base import create_table
from views.forms import CreateAccountForm, CreateUserForm, FirstLogin, UpdateCategories, BalanceForm
templates = Jinja2Templates(directory='templates')


async def transaction_add_form(request):
    user = request.session.get("user")
    category = Categories()
    print(user)
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('add_transaction.html')
        categories = await category.get_user_categories(user['sub'])
        form = await CreateAccountForm.from_formdata(request)
        if categories is not None:
            form.categories.choices = [c.name for c in categories]
        else:
            form.categories.choices = "Test"
        html = template.render(form=form)
        return HTMLResponse(html)
    elif 'id' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('add_transaction.html')
        form = await CreateAccountForm.from_formdata(request)
        now = datetime.utcnow()
        form.date_added = datetime.strptime(now, "%Y-%m-%d %H:%M:%S").date()
        print(form.date_added)
        if form.validate_on_submit():
            html = template.render(form=form)
            return HTMLResponse(html)
    else:
        return RedirectResponse("/login")


async def add_transaction_response(request):
    session_user = request.session.get("user")
    data = await request.form()
    print(f'data is {data}')
    user = User()
    category = Categories()
    transaction = Transactions()
    if 'sub' in session_user:
        print(data)
        current_balance = await user.get_balance(user_id=session_user['sub'])
        new_balance = (current_balance - float(data['transaction']))
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f'now is {now}')
        print(datetime.strptime(now, "%Y-%m-%d %H:%M:%S").date())
        print(await category.get_category_id(session_user['sub']))
        await transaction.add_transaction(amount=data['transaction'],
                                          recipient=data['recipient'],
                                          note=data['note'],
                                          date_of_transaction=datetime.strptime(
            data['date_of_transaction'], "%Y-%m-%d"),
            user_id=session_user['sub'],
            categories=data['categories'],
            date_added=datetime.utcnow()
        )

    elif 'id' in session_user:
        await transaction.add_transaction(data['transaction'],
                                          note=data['note'],
                                          date_of_transaction=datetime.strptime(
            data['date_of_transaction'], "%Y-%m-%d"),
            user_id=session_user['id'],
            categories=data['categories']
        )
    return RedirectResponse('/budget')
