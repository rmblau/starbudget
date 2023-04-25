from jinja2 import FileSystemLoader, Environment
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette_core.paginator import Paginator

import budgeting.user
from budgeting.categories import (
    create_category, get_category_balance, update_category_balance, update_category_name, get_unhidden_user_categories
)
from budgeting.transaction import get_transaction_by_category
from budgeting.user import get_balance, update_balance
from views.forms import UpdateCategories, CreateCategories

templates = Jinja2Templates(directory='templates')


async def categories(request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse('/auth/login')
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('categories.html')
        categories = await get_unhidden_user_categories(user['sub'])
        form = await UpdateCategories.from_formdata(request)
        context = {"request": request, "categories":
            [c.name for c in categories], "balance": [c.balance for c in categories], "form": form}
        return templates.TemplateResponse(template, context=context)


async def create_category(request):
    user = request.session.get("user")
    data = await request.form()
    bank_balance = await get_balance(user['sub'])
    if 'sub' in user:
        await budgeting.categories.create_category(user['sub'], data['category'], balance=float(data['balance']))
        new_balance = float(bank_balance) - float(data['balance'])
        await update_balance(user['sub'], new_balance)
        return RedirectResponse('/categories')
    return RedirectResponse("/auth/login")


async def category_response(request):
    user = request.session.get("user")
    template = "category_detail.html"

    if 'sub' in user:
        data = await request.form()
        if 'btnRenameCategory' in data:
            await update_category_name(new_name=data['newname'], old_name=data['oldname'], user_id=user['sub'])
        elif 'btnCategoryDetail' in data:
            category_data = await get_category_balance(f"{data['oldname']}~{user['sub']}", user['sub'])
            context = {"request": request, "details": category_data}
            return templates.TemplateResponse(template, context)
        else:
            return RedirectResponse('/categories')
    else:
        return RedirectResponse('/auth/login')
    return RedirectResponse('/categories')


async def category_detail(request):
    user = request.session.get("user")
    template = "category_detail.html"
    if user is None:
        return RedirectResponse("auth/login")
    if 'sub' in user:
        category_detail = await get_category_balance(f"{request.path_params['category']}~{user['sub']}",
                                                     user['sub'])
        category_transactions = await get_transaction_by_category(user['sub'],
                                                                  f"{request.path_params['category']}~{user['sub']}")
        categories = await get_unhidden_user_categories(user_id=user['sub'])
        paginator = Paginator(category_transactions, 10)
        page_number = request.query_params.get("page", 1)
        page = paginator.get_page(page_number)
        print(f'{request.path_params["category"]}')
        context = {"request": request, "categories": [c.name for c in categories], "amount_remaining": category_detail,
                   "category": f"{request.path_params['category']}~{user['sub']}",
                   "paginator": paginator,
                   "page": page}
        return templates.TemplateResponse(template, context)


async def add_to_category_balance(amount, user_id, category_name):
    balance = await get_balance(user_id)
    current_category_balance = await get_category_balance(f'{category_name}~{user_id}', user_id)
    amount_to_add = amount
    new_category_balance = float(amount_to_add) + current_category_balance
    new_balance = float(balance) - float(amount)
    updated_category_balance = await update_category_balance(f'{category_name}~{user_id}', user_id, new_category_balance)
    updated_balance = await update_balance(user_id, new_balance)
    category_balance = await get_category_balance(category_name, user_id)
    print(f"{category_balance=} in add function")
    balance = await get_balance(user_id)
    return category_balance, balance

async def subtract_from_category_balance(amount, user_id, category_name):
    balance = await get_balance(user_id)
    current_category_balance = await get_category_balance(f'{category_name}~{user_id}', user_id)
    new_category_balance = current_category_balance - float(amount)
    new_balance = float(balance)  + float(amount)
    updated_category_balance = await update_category_balance(f'{category_name}~{user_id}', user_id, new_category_balance)
    category_balance = await get_category_balance(category_name, user_id)
    updated_balance = await update_balance(user_id, new_balance)
    balance = await get_balance(user_id)
    return category_balance, balance

async def move_to_category(amount, user_id, move_from, move_to):
    cateogry_balance, balance = await subtract_from_category_balance(amount, user_id, f'{move_from}~{user_id}')
    await add_to_category_balance(amount, user_id, f'{move_to}~{user_id}')

async def update_category_balance_request(request):
    user = request.session.get("user")
    category_name = f"{request.path_params['category']}"
    if 'sub' in user:
        data = await request.form()
        print(f'{data=}')
        if 'btnUpdateTransaction' in data:
            current_category_balance = await get_category_balance(f'{category_name}~{user["sub"]}', user["sub"])
            category_balance, balance = await add_to_category_balance(data['balanceAmount'], user['sub'], category_name)
            await update_category_balance(category_name, user['sub'], category_balance)
            await update_balance(user['sub'], balance)
        elif 'btnDeleteTransaction' in data:
            current_category_balance = await get_category_balance(f'{category_name}~{user["sub"]}', user["sub"])
            category_balance, balance = await subtract_from_category_balance(data['balanceAmount'], user['sub'], category_name)
            await update_category_balance(category_name, user['sub'], category_balance)
            await update_balance(user['sub'], balance)
        return RedirectResponse(f"/{category_name}")
    return RedirectResponse("auth/login")


async def delete_category(request):
    user = request.session.get("user")
    data = await request.form()

    if 'sub' in user:
        category_balance = await get_category_balance(f"{data['oldname']}~{user['sub']}", user['sub'])
        bank_balance = await get_balance(user['sub'])
        new_balance = float(bank_balance) + category_balance
        await budgeting.categories.delete_category(f"{data['oldname']}~{user['sub']}", user['sub'])
        await update_balance(user['sub'], new_balance)
        return RedirectResponse('/categories')
    return RedirectResponse('/auth/login')


async def create_category_form(request):
    template = "category.html"
    form = await CreateCategories.from_formdata(request)
    context = {"request": request, "form": form}
    return templates.TemplateResponse(template, context)
