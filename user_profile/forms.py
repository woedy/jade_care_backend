from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from user_profile.models import PersonalInfo

User = get_user_model()



class PersonalInfoForm(forms.ModelForm):



    class Meta:
        model = PersonalInfo
        fields = ('country', 'gender', 'photo', 'dob', 'marital_status', 'phone')



class EditProfileForm(forms.ModelForm):



    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')



EditProfileFormInlineFormset = inlineformset_factory(
    User,
    PersonalInfo,
    form=PersonalInfoForm,
    extra=1,
)