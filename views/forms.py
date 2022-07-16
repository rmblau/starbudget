from starlette_wtf import StarletteForm
from wtforms import StringField, DateField, SelectField, DecimalField, FieldList, SubmitField
from wtforms.widgets import SubmitInput
from wtforms.validators import DataRequired


class CreateAccountForm(StarletteForm):
    transaction = StringField(
        'Transaction amount',
        validators=[
            DataRequired('Amount')
        ]
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
        ]
    )


class BalanceForm(StarletteForm):
    balance = StringField(
        'Category Namet',
        validators=[
            DataRequired('Amount')
        ]
    )
