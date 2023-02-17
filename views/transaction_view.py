from datetime import datetime
from budgeting.categories import (
    get_category_balance,
    update_category_balance, get_category_id
)
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse

from budgeting.transaction import add_transaction, edit_transaction, get_transaction_id, delete_transaction
from budgeting.user import get_balance, add_income, get_income, update_balance
from views.forms import TransactionForm
templates = Jinja2Templates(directory='templates')


async def transaction_add_form(request):
    user = request.session.get("user")
    print(user)
    if 'sub' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('add_transaction.html')
        form = await TransactionForm.from_formdata(request)
        html = template.render(form=form)
        return HTMLResponse(html)
    elif 'id' in user:
        env = Environment()
        env.loader = FileSystemLoader('./templates')
        template = env.get_template('add_transaction.html')
        form = await TransactionForm.from_formdata(request)
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
    if 'sub' in session_user:
        print(data)
        
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f'now is {now}')
        print(datetime.strptime(now, "%Y-%m-%d %H:%M:%S").date())
        print(await get_category_id(session_user['sub']))
        await add_transaction(amount=data['transaction'],
                                          recipient=data['recipient'],
                                          note=data['note'],
                                          date_of_transaction=datetime.strptime(
            data['date_of_transaction'], "%Y-%m-%d"),
            user_id=session_user['sub'],
            categories=data['categories'],
            date_added=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f"))
        bank_balance = await get_balance(session_user['sub'])
        category_balance = await get_category_balance(f"{data['categories']}~{session_user['sub']}", session_user['sub'])
        new_category_balance = category_balance - float(data['transaction'])
        if new_category_balance < 0:
            #this is a negative number so add to the balance
            new_balance = bank_balance + new_category_balance
            await update_balance(session_user['sub'], new_balance)
        print(f"new category balance {new_category_balance=}")
        updated_category = await update_category_balance(f"{data['categories']}~{session_user['sub']}", session_user['sub'], new_category_balance)
        print(f"{updated_category=}")
    return RedirectResponse('/budget')


async def update_or_delete_transaction(request):
    session_user = request.session.get("user")
    if session_user is not None:
        if 'sub' in session_user:
            data = await request.form()
            print(f"{data=}")
            old_date = datetime.strptime(
                data['olddate'], "%Y-%m-%d").date()
            submit_time = data['submitTime']
            date = datetime.strptime(
                data['date'], "%Y-%m-%d").date()
            print(f"submit time: {data['submitTime']}")
            if 'btnUpdateTransaction' in data:
                transaction_id = await get_transaction_id(user_id=str(session_user['sub']),
                                                          recipient=str(data['old_recipient']),
                                                          amount=float(data['oldamount']),
                                                          note=data['oldname'],
                                                          date=date,
                                                          category=data['old-category'],
                                                          submit_time=submit_time)
                await edit_transaction(recipient=data['newrecipient'],
                                       amount=float(data['newamount']),
                                       note=data['newname'],
                                       date_of_transactions=date,
                                       user_id=session_user['sub'],
                                       old_category_id=transaction_id,
                                       categories=data['category'],
                                       submit_time=submit_time)

                category_balance = await get_category_balance(data['old-category'], session_user['sub'])
                print(f"{data['oldamount']}")
                if float(data['oldamount']) > float(data['newamount']):
                    new_category_balance = category_balance + (float(data['oldamount']) - float(data['newamount']))
                    print(f'{new_category_balance=}')
                    print(data['category'])
                    await update_category_balance(data['category'], session_user['sub'], new_category_balance)
                else:
                    new_category_balance = category_balance - (float(data['newamount']) - float(data['oldamount']))
                    print(f'{new_category_balance=} old amount is less than new amount')
                    await update_category_balance(data['category'], session_user['sub'], new_category_balance)

            elif 'btnDeleteTransaction' in data:
                category_balance = await get_category_balance(data['old-category'], session_user['sub'])
                transaction_id = await get_transaction_id(user_id=str(session_user['sub']),
                                                          recipient=str(data['old_recipient']),
                                                          amount=float(data['oldamount']),
                                                          note=data['oldname'],
                                                          date=old_date,
                                                          category=data['old-category'],
                                                          submit_time=data['submitTime'])

                bank_balance = await get_balance(session_user['sub'])
                new_bank_balance = bank_balance + float(data['oldamount'])
                await update_balance(session_user['sub'], new_bank_balance)
                await delete_transaction(
                    str(session_user['sub']), int(transaction_id))
                new_category_balance = category_balance + (float(data['oldamount']))
                await update_category_balance(data['category'], session_user['sub'], new_category_balance)
            return RedirectResponse("/budget")

async def income_add_response(request):
    session_user = request.session.get("user")
    data = await request.form()
    if 'sub' in session_user:
        print(f'{data=}')
        await add_income(session_user['sub'], amount=float(data['amount']), source=data['source'], date=datetime.strptime(data['date'], "%Y-%m-%d"), date_added=datetime.today().strftime("%Y-%m-%d"))
        old_balance = await get_balance(user_id=session_user['sub'])
        print(old_balance)
        income = await get_income(session_user['sub'])
        new_balance = old_balance + income
        print(f'{new_balance=}')
        await update_balance(session_user['sub'], new_balance)
    return RedirectResponse('/dashboard')
