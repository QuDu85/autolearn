from django.forms import ModelForm
from api.models import Material, Student

# Create the form class.
class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'skill', 'length', 'link','image','topic','language','level','description']
        
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MaterialForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['skill'].required = False
        self.fields['language'].required = False
        self.fields['level'].required = False
        