from django import forms
from planner.models import Map


class MapForm(forms.Form):

    maps = forms.ModelMultipleChoiceField(queryset=Map.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)

        self.fields['maps'].widget.attrs.update({'class': 'form-control'})
