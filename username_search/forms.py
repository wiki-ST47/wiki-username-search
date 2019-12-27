from django import forms


class SearchForm(forms.Form):
    wiki_url = forms.CharField(
        label="Path to the wiki",
        required=False,
    )
    search = forms.CharField(
        label="Search query",
    )
    to_search = forms.IntegerField(
        label="Maximum number of users to return",
        required=False,
    )
    case_sensitive = forms.TypedChoiceField(
        label="Case sensitive?",
        choices=((True, "Yes"), (False, "No")),
        initial=True,
        coerce=lambda x: x == 'True',
    )
    regex = forms.TypedChoiceField(
        label="Regular expression search?",
        choices=((True, "REGEXP"), (False, "LIKE")),
        initial=True,
        coerce=lambda x: x == 'True',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
