from wtforms import Form, StringField

class QuerySearchForm(Form):
    search = StringField('')