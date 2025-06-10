from django import forms
from .models import Query

class UserQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['name','email','contact','message']

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user',None)
        super(UserQueryForm,self).__init__(*args,**kwargs)

        if user:
            profile = user.userprofile
            full_name = f'{profile.first_name} {profile.last_name}'
            self.fields['name'].initial = full_name
            self.fields['email'].initial =user.email                 
            self.fields['contact'].initial = profile.contact    
            for field in ['name','email','contact']:
                self.fields[field].disabled = True

class SponsorQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['name','organisation', 'email','contact','message']
