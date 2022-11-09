from jinja2 import FileSystemLoader, Environment
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette_core.paginator import Paginator

from budgeting.categories import Categories
from budgeting.transaction import get_transaction_by_category
from budgeting.user import get_balance, update_balance
from views.forms import UpdateCategories, CreateCategories

templates = Jinja2Templates(directory='templates')


async def categories(request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse('/auth/login')
    category = Categories()
    categories = await category.get_unhidden_user_categories(user['sub'])
    template = "categories.html"
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('categories.html')
        categories = await category.get_unhidden_user_categories(user['sub'])
        print(categories)
        form = await UpdateCategories.from_formdata(request)
        context = {"request": request, "categories":
            [c.name for c in categories], "balance": [c.balance for c in categories], "form": form}
        return templates.TemplateResponse(template, context=context)


async def create_category(request):
    categories = Categories()
    user = request.session.get("user")
    data = await request.form()
    bank_balance = await get_balance(user['sub'])
    print(f'data from the form is {data}')
    if 'sub' in user:
        response = await categories.create_category(user['sub'], data['category'], balance=data['balance'])
        new_balance = bank_balance - float(data['balance'])
        await update_balance(user['sub'], new_balance)
        return RedirectResponse('/categories')
    return RedirectResponse("/auth/login")


async def category_response(request):
    category = Categories()

    user = request.session.get("user")
    template = "category_detail.html"
    print(f'request is {await request.form()}')
    button_click = request.get("btnRenameCategory", False)
    print(request.get("btnDetail"))
    print(f'button clicked is {button_click}')
    print(user)

    if 'sub' in user:
        data = await request.form()
        if 'btnRenameCategory' in data:
            print('rename found')
            print(data['newname'])
            await category.update_category_name(new_name=data['newname'], old_name=data['oldname'], user_id=user['sub'])
        elif 'btnCategoryDetail' in data:
            print('detail found')
            category_data = await category.get_category_balance(f"{data['oldname']}~{user['sub']}", user['sub'])
            context = {"request": request, "details": category_data}
            return templates.TemplateResponse(template, context)
        else:
            print("Not found")
        print(f'data is {data}')
        return RedirectResponse('/categories')
    return RedirectResponse('/auth/login')


async def category_detail(request):
    user = request.session.get("user")
    categories = Categories()
    data = await request.form()
    template = "category_detail.html"
    if 'sub' in user:
        category_detail = await categories.get_category_balance(f"{request.path_params['category']}~{user['sub']}",
                                                                user['sub'])
        category_transactions = await get_transaction_by_category(user['sub'],
                                                                  f"{request.path_params['category']}~{user['sub']}")
        categories = await categories.get_unhidden_user_categories(user_id=user['sub'])
        paginator = Paginator(category_transactions, 10)
        page_number = request.query_params.get("page", 1)
        page = paginator.get_page(page_number)
        context = {"request": request, "categories": [c.name for c in categories], "amount_remaining": category_detail,
                   "paginator": paginator,
                   "page": page}
        return templates.TemplateResponse(template, context)


async def delete_category(request):
    category = Categories()

    user = request.session.get("user")
    print(user)
    data = await request.form()
    print(data)

    if 'sub' in user:
        category_balance = await category.get_category_balance(f"{data['oldname']}~{user['sub']}", user['sub'])
        bank_balance = await get_balance(user['sub'])
        new_balance = bank_balance + category_balance
        await category.delete_category(f"{data['oldname']}~{user['sub']}", user['sub'])
        await update_balance(user['sub'], new_balance)

        return RedirectResponse('/categories')
    return RedirectResponse('/auth/login')


async def create_category_form(request):
    template = "category.html"
    form = await CreateCategories.from_formdata(request)
    context = {"request": request, "form": form}
    return templates.TemplateResponse(template, context)
