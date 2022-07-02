from budgeting.budget import Budget

from starlette.responses import JSONResponse


async def get_transactions(request):
    budget = Budget()
    transactions = await budget.get_transaction(user_id=1)
    return JSONResponse({"Transactions": transactions})
