from django.forms import Form, CharField

class UserSearchForm(Form):
    '''Form for the task search bar'''
    query = CharField(max_length=100)

    query.widget.attrs.update({'placeholder': 'Search all tasks...'})