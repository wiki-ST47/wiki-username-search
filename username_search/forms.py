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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
