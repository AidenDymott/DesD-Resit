from django import forms
from django.forms import CheckboxInput, ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Showing, Screen, ClubAccount, Booking


from django.contrib.auth.models import User

# Registration Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'auth-input2'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['first_name'].widget.attrs['class'] = 'auth-input2'

        self.fields['last_name'].widget.attrs['class'] = 'auth-input2'

        self.fields['email'].widget.attrs['class'] = 'auth-input2'

        self.fields['password1'].widget.attrs['class'] = 'auth-input2'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'auth-input2'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''

# Register Club Form
class ClubRegistration(ModelForm):
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())
    
    class Meta:
        model = ClubAccount
        fields = ['club_name', 'landline', 'mobile', 'email', 'street_number', 'street', 'city', 'post_code', 'club_rep', 'password1', 'password2']
        
        def __init__(self, *args, **kwargs):
            super(ClubRegistration, self).__init__(*args, **kwargs)
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Required.</small></span>'
            
            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Passwords didn\'t match.</small></span>'

# Create Movie Form
class MovieForm(ModelForm):   
    class Meta:
        model = Movie
        fields = ('movie_name', 'movie_image', 'description', 'rating')
    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
  
        self.fields['movie_name'].widget.attrs['class'] = 'form-control'
        self.fields['movie_name'].widget.attrs['placeholder'] = 'Movie Name'
        self.fields['movie_name'].label = ''
  
        self.fields['movie_image'].widget.attrs['class'] = 'form-control'  		
        self.fields['movie_image'].widget.attrs['placeholder'] = 'Movie Image'
        self.fields['movie_image'].label = ''
  
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Movie Description'
        self.fields['description'].label = ''
  
        self.fields['rating'].widget.attrs['class'] = 'form-control'
        self.fields['rating'].widget.attrs['placeholder'] = 'Movie Rating'
        self.fields['rating'].label = ''
  
# Create Movie Showing Form
class DateInput(forms.DateInput):
    input_type ='date'

class ShowingForm(ModelForm):   
    class Meta:
        model = Showing
        fields = ('movie', 'date_showing', 'time_showing', 'screen', 'social_distance')
        widgets = {'date_showing': DateInput()}
    def __init__(self, *args, **kwargs):
        super(ShowingForm, self).__init__(*args, **kwargs)
  
        self.fields['movie'].widget.attrs['class'] = 'form-control'
        self.fields['movie'].widget.attrs['placeholder'] = 'Movie'
        self.fields['movie'].label = ''
  
        self.fields['date_showing'].widget.attrs['class'] = 'form-control'
        self.fields['date_showing'].widget.attrs['placeholder'] = 'Showing Date, YYYY/MM/DD'
        self.fields['date_showing'].label = ''
  
        self.fields['time_showing'].widget.attrs['class'] = 'form-control'
        self.fields['time_showing'].widget.attrs['placeholder'] = 'Showing Time, XX:XX:XX'
        self.fields['time_showing'].label = ''

        self.fields['screen'].widget.attrs['class'] = 'form-control'
        self.fields['screen'].widget.attrs['placeholder'] = 'Screen'
        self.fields['screen'].label = ''
  
class ScreenForm(ModelForm):
    class Meta:
        model = Screen
        fields = ('screen_num', 'rows', 'columns')
    def __init__(self, *args, **kwargs):
        super (ScreenForm, self).__init__(*args, **kwargs)
        self.fields['screen_num'].widget.attrs['class'] = 'form-control'
        self.fields['screen_num'].widget.attrs['placeholder'] = 'Screen Number'
        self.fields['screen_num'].label = ''
    
class BookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        showing = kwargs.pop('showing')
        super().__init__(*args, **kwargs)
        seats = showing.seat_layout

        for seat in seats:
            if seat['is_available']:
                self.fields[seat['seat_num']] = forms.BooleanField(
                    required=False,
                    widget=forms.CheckboxInput())
            else:
                self.fields[seat['seat_num']] = forms.BooleanField(
                    required=False, 
                    widget=forms.CheckboxInput(attrs={'disabled': 'disabled'}))
