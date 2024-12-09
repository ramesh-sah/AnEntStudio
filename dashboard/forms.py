## Django imports
from django import forms
from django.contrib.auth import get_user_model

## Local Imports
from api.models import (Slider, Add, Event, Category, Genre, VideoCategory, EventVotingSettings,
                        UserEventVoting, OrganizationSetting, VideoMenu, Album, AlbumImage,
                        PrivacyAndPolicy, TermsAndCondition)

''''Slider form'''
class SliderForm(forms.ModelForm):
    class Meta:
        model  = Slider
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(SliderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

''''Ads form'''
class AdsForm(forms.ModelForm):
    class Meta:
        model  = Add
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(AdsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

''''Category form'''
class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

''''Event genre form'''
class GenreForm(forms.ModelForm):
    class Meta:
        model  = Genre
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

'''Event form'''
class EventForm(forms.ModelForm):
    participate_start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',  # HTML5 input type for date-time
                'class': 'form-control',
                'placeholder': 'Select participation start time'
            }
        ),
        required=False  # Adjust as needed
    )
    participate_end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Select participation end time'
            }
        ),
        required=False
        
        
    )
    voting_start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Select voting start time'
            }
        ),
        required=False
    )
    voting_end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Select voting end time'
            }
        ),
        required=False
    )
        
    contest_start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',  # HTML5 input type for date-time
                'class': 'form-control',
                'placeholder': 'Select contest start time'
            }
        ),
        required=False  # Adjust as needed
    )
    contest_end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Select contest end time'
            }
        ),
        required=False
    )
    event_date = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                'type': 'datetime-local',  # HTML5 date input
                'class': 'form-control',
                'placeholder': 'Select event date'
            }
        ),
        required=False  # Adjust as needed
    )
    class Meta:
        model  = Event
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

        # Set rows and cols for the description field
        self.fields['description'].widget.attrs['rows'] = 3  # Set number of rows
        self.fields['description'].widget.attrs['cols'] = 40  # Set number of columns


''''Video Category form'''
class VideoCategoryForm(forms.ModelForm):
    class Meta:
        model  = VideoCategory
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(VideoCategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

''''Voting detail of event form'''
class VotingForm(forms.ModelForm):
    class Meta:
        model  = EventVotingSettings
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(VotingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

''''Voting user detail of event form'''
class VotingUserForm(forms.ModelForm):
    class Meta:
        model  = UserEventVoting
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(VotingUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'

class OrganizationSettingForm(forms.ModelForm):
    class Meta:
        model = OrganizationSetting
        fields = '__all__'

''''Video form'''
class VideoMenuForm(forms.ModelForm):
    class Meta:
        model  = VideoMenu
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(VideoMenuForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'


'''Album form'''
class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'
class AlbumImageForm(forms.ModelForm):
    class Meta:
        model = AlbumImage
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super(AlbumImageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f"Enter {field_name}"
            field.widget.attrs['class'] = 'form-control'


class PrivacyAndPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyAndPolicy
        fields = '__all__'

class TermsAndConditionForm(forms.ModelForm):
    class Meta:
        model = TermsAndCondition
        fields = '__all__'


### Login form
class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())