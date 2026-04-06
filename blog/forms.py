from django import forms
from .models import Contact


# class ContactForm(forms.Form):
#     name    = forms.CharField(max_length=100)
#     email   = forms.EmailField()
#     message = forms.CharField(widget=forms.Textarea)






class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

    #  Name validation
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name




    # Email duplicate check and name can change 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Contact.objects.filter(email=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("This email already exists.")

        return email
    




    # Message length validation
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must contain at least 10 characters.")
        return message









