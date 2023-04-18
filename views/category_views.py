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
        await budgeting.categories.create_category(user['sub'], data['category'], balance=data['balance'])
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
    return RedirectResponse('/auth/login')


async def category_detail(request):
    user = request.session.get("user")
    template = "category_detail.html"
    if 'sub' in user:
        category_detail = await get_category_balance(f"{request.path_params['category']}~{user['sub']}",
                                                     user['sub'])
        category_transactions = await get_transaction_by_category(user['sub'],
                                                                  f"{request.path_params['category']}~{user['sub']}")
        categories = await get_unhidden_user_categories(user_id=user['sub'])
        paginator = Paginator(category_transactions, 10)
        page_number = request.query_params.get("page", 1)
        page = paginator.get_page(page_number)
        context = {"request": request, "categories": [c.name for c in categories], "amount_remaining": category_detail,
                   "category": f"{request.path_params['category']}~{user['sub']}",
                   "paginator": paginator,
                   "page": page}
        return templates.TemplateResponse(template, context)


async def update_category_balance_request(request):
    user = request.session.get("user")
    category_name = f"{request.path_params['category']}"
    if 'sub' in user:
        data = await request.form()
        current_category_balance = await get_category_balance(f'{category_name}~{user["sub"]}', user["sub"])
        if float(data['balanceAmount']) >= current_category_balance:
            balance = await get_balance(user["sub"])
            new_balance = balance - float(data['balanceAmount'])
            await update_balance(user["sub"], new_balance)
        elif float(data['balanceAmount']) == 0:
            balance = await get_balance(user['sub'])
            new_balance = balance + current_category_balance
            await update_balance(user['sub'], new_balance)
        else:
            balance = await get_balance(user["sub"])
            new_balance = balance + float(data['balanceAmount'])
            await update_balance(user["sub"], new_balance)
        await update_category_balance(category=f'{category_name}~{user["sub"]}', user_id=user['sub'], balance=data['balanceAmount'])

        return RedirectResponse(f"/category_detail/{category_name}")
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
