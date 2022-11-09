from unicodedata import category
from starlette_wtf import StarletteForm
from wtforms import StringField, DateField, SelectField, DecimalField, FieldList, SubmitField, HiddenField
from wtforms.widgets import SubmitInput
from wtforms.validators import DataRequired, InputRequired, NumberRange


class TransactionForm(StarletteForm):
    transaction = DecimalField(
        'Transaction amount',
        validators=[
            InputRequired('Amount')
        ]
    )
    recipient = StringField(
        'Paid to',
        validators=[InputRequired('Recipient')]
    )
    note = StringField(
        'Transaction notes',
        validators=[DataRequired('Note')]
    )
    date_of_transaction = DateField('DatePicker',
                                    validators=[DataRequired('Date')],
                                    format="%Y-%m-%d"
                                    )
    categories = SelectField('SelectField', validators=[
                             DataRequired('categories')])
    date_added = HiddenField(DateField('DatePicker', validators=[DataRequired('Date')
                                                                 ], format="%Y-%m-%d %H:%M:%S"))


class CreateUserForm(StarletteForm):
    name = StringField(
        'Name of user',
        validators=[
            DataRequired('Name')
        ]
    )
    categories = StringField(
        'Category',
        validators=[DataRequired('Category')]
    )
    balance = DecimalField('Balance', validators=[DataRequired("Balance")])


class UpdateCategories(StarletteForm):
    categories = StringField(
        'Category Name',
        validators=[
            DataRequired('Amount')
        ]
    )
    submit = SubmitField(label=f"Update")


class CreateCategories(StarletteForm):
    categories = StringField(
        'Category Name',
        validators=[
            DataRequired('Categories')
        ]
    )


class FirstLogin(StarletteForm):
    balance = DecimalField('Balance', validators=[DataRequired("Balance")])
    categories = StringField(
        'Category Name',
        validators=[
            DataRequired('Category Name')
        ])
    category_balance = DecimalField("Category Balance", validators=[DataRequired("Category Balance")])


class BalanceForm(StarletteForm):
    balance = DecimalField(
        'Category Name',
        validators=[
            DataRequired('Amount')
        ]
    )


class IncomeForm(StarletteForm):
    amount = DecimalField(
        "Income",
        validators=[DataRequired("Income Amount"), NumberRange(min=0)]
    )
    source = StringField("Source of income", validators=[DataRequired("Source")]
    )
    date = DateField('DatePicker',
                                    validators=[DataRequired('Date')],
                                    format="%Y-%m-%d"
                                    )