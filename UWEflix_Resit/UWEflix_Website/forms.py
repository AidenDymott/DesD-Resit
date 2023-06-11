from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Showing


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

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required.</small></span>'

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
		fields = ('movie_name', 'description', 'rating')
	def __init__(self, *args, **kwargs):
		super(MovieForm, self).__init__(*args, **kwargs)
  
		self.fields['movie_name'].widget.attrs['class'] = 'form-control'
		self.fields['movie_name'].widget.attrs['placeholder'] = 'Movie Name'
		self.fields['movie_name'].label = ''
  
		self.fields['description'].widget.attrs['class'] = 'form-control'
		self.fields['description'].widget.attrs['placeholder'] = 'Movie Description'
		self.fields['description'].label = ''
  
		self.fields['rating'].widget.attrs['class'] = 'form-control'
		self.fields['rating'].widget.attrs['placeholder'] = 'Movie Rating'
		self.fields['rating'].label = ''
  
# Create Movie Showing Form
class ShowingForm(ModelForm):   
	class Meta:
		model = Showing
		fields = ('movie', 'date_showing', 'time_showing', 'seats')
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
  
		self.fields['seats'].widget.attrs['class'] = 'form-control'
		self.fields['seats'].widget.attrs['placeholder'] = 'Seats'
		self.fields['seats'].label = ''
  
  # Create Movie Showing Form
class BookingForm(ModelForm):   
	class Meta:
		model = Showing
		fields = ('movie', 'date_showing', 'time_showing', 'seats')
	def __init__(self, *args, **kwargs):
		super(BookingForm, self).__init__(*args, **kwargs)
  
		self.fields['movie'].widget.attrs['class'] = 'form-control'
		self.fields['movie'].widget.attrs['placeholder'] = 'Movie'
		self.fields['movie'].label = ''
  
		self.fields['date_showing'].widget.attrs['class'] = 'form-control'
		self.fields['date_showing'].widget.attrs['placeholder'] = 'Showing Date'
		self.fields['date_showing'].label = ''
  
		self.fields['time_showing'].widget.attrs['class'] = 'form-control'
		self.fields['time_showing'].widget.attrs['placeholder'] = 'Showing Time'
		self.fields['time_showing'].label = ''
  
		self.fields['seats'].widget.attrs['class'] = 'form-control'
		self.fields['seats'].widget.attrs['placeholder'] = 'Seats'
		self.fields['seats'].label = ''
  
  
  


        
        
         
	
    
        
    