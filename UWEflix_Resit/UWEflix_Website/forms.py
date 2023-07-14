from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Movie, Showing, Screen, Club, Ticket
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

        self.fields['username'].widget.attrs['class'] = 'auth-input'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['first_name'].widget.attrs['class'] = 'auth-input'
        self.fields['last_name'].widget.attrs['class'] = 'auth-input'
        self.fields['email'].widget.attrs['class'] = 'auth-input'

        self.fields['password1'].widget.attrs['class'] = 'auth-input'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'auth-input'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''

# Register Club Form
class ClubForm(ModelForm):
    class Meta:
        model = Club
        fields = ('club_name', 'landline', 'mobile', 'street_number', 'street',
                  'city', 'post_code')

    def __init__(self, *args, **kwargs):
        super(ClubForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.label = False
            field.widget.attrs['class'] = 'auth-input'

        self.fields['club_name'].widget.attrs['placeholder'] = 'Club Name'
        self.fields['landline'].widget.attrs['placeholder'] = 'Landline'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Mobile'
        self.fields['street_number'].widget.attrs['placeholder'] = 'Street Number'
        self.fields['street'].widget.attrs['placeholder'] = 'Street'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['post_code'].widget.attrs['placeholder'] = 'Postcode'

# Create Movie Form
class MovieForm(ModelForm):   
    RATING_CHOICES = (
            ('U', 'U'),
            ('PG', 'PG'),
            ('12A', '12A'),
            ('12', '12'),
            ('15', '15'),
            ('18', '18'),
            ('R18', 'R18'),
        )
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Movie Rating')

    class Meta:
        model = Movie
        fields = ('movie_name', 'movie_image', 'duration', 'description', 'rating')

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
  
        self.fields['movie_name'].widget.attrs['class'] = 'form-control'
        self.fields['movie_name'].widget.attrs['placeholder'] = 'Movie Name'
        self.fields['movie_name'].label = ''
  
        self.fields['movie_image'].widget.attrs['class'] = 'form-control'  		
        self.fields['movie_image'].widget.attrs['placeholder'] = 'Movie Image'
        self.fields['movie_image'].label = ''

        self.fields['duration'].widget.attrs['placeholder'] = 'Duration (mins)'
        self.fields['duration'].label = ''
  
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Movie Description'
        self.fields['description'].label = ''
  
        self.fields['rating'].widget.attrs['class'] = 'form-control'
        self.fields['rating'].widget.attrs['placeholder'] = 'Movie Rating'
        self.fields['rating'].label = 'Movie Rating'
  
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

        self.fields['rows'].widget.attrs['placeholder'] = 'Rows'
        
        self.fields['columns'].widget.attrs['placeholder'] = 'Seats per row'
        self.fields['columns'].label = 'Seats per row'
    
class BookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        showing = kwargs.pop('showing')
        super().__init__(*args, **kwargs)
        seats = showing.seat_layout

        for seat in seats:
            if seat['is_available']:
                self.fields[seat['seat_num']] = forms.BooleanField(
                    required=False,
                    widget=forms.CheckboxInput(attrs={'class': 'booking-seat-available'}))
            else:
                self.fields[seat['seat_num']] = forms.BooleanField(
                    required=False, 
                    widget=forms.CheckboxInput(attrs={'disabled': 'disabled',
                                                      'class': 'booking-seat-reserved'}))

class PaymentForm(forms.Form):
    card_name = forms.CharField(max_length=50)
    card_number = forms.CharField(max_length=16)
    card_expire = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    card_cvv = forms.CharField(max_length=3)
    children = forms.IntegerField(label='Children')
    adults = forms.IntegerField(label='Adults')
    students = forms.IntegerField(label='Students')
        
    def __init__(self, *args, **kwargs):
        super (PaymentForm, self).__init__(*args, **kwargs)
        self.initial['children'] = 0
        self.initial['students'] = 0
        self.initial['adults'] = 0

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'payment-input'

        self.fields['card_name'].widget.attrs['placeholder'] = 'Cardholder Name'
        self.fields['card_number'].widget.attrs['placeholder'] = 'Card Number'
        self.fields['card_expire'].widget.attrs['placeholder'] = 'Card Expiry'
        self.fields['card_cvv'].widget.attrs['placeholder'] = 'CVV'
        self.fields['children'].widget.attrs['placeholder'] = 'Number of children'
        self.fields['adults'].widget.attrs['placeholder'] = 'Number of adults'
        self.fields['students'].widget.attrs['placeholder'] = 'Number of students'
        
class ClubPaymentForm(forms.Form):
    card_name = forms.CharField(max_length=50)
    card_number = forms.CharField(max_length=16)
    card_expire = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    card_cvv = forms.CharField(max_length=3)
    amount = forms.IntegerField()
       
    def __init__(self, *args, **kwargs):
        super (ClubPaymentForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'payment-input'

        self.fields['card_name'].widget.attrs['placeholder'] = 'Cardholder Name'
        self.fields['card_number'].widget.attrs['placeholder'] = 'Card Number'
        self.fields['card_expire'].widget.attrs['placeholder'] = 'Card Expiry'
        self.fields['card_cvv'].widget.attrs['placeholder'] = 'CVV'
        self.fields['amount'].widget.attrs['placeholder'] = 'Amount'

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('child', 'student', 'adult')

    child = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'Child'}))
    student = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'Student'}))
    adult = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'Adult'}))

    def __init__(self, *args, **kwargs):
        super (TicketForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.label = False
            field.widget.attrs['class'] = 'payment-input'
