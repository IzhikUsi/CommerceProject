from django import forms

from .models import *

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
                    'title': forms.TextInput(attrs={'class': 'form-control'}),
                    'description': forms.Textarea(attrs={'rows':2, 'maxlength': 1000, 'class': 'form-control'}),
                    'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
                    'image': forms.URLInput(attrs={'class': 'form-control'}),
                    'category': forms.Select(attrs={'class': 'form-control'})
                    }
        labels = {
            'image': 'Image URLs'
        }

                    

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        lables = {
            'comment': ''
        }
        widgets = {'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'maxlength': '5000'})}
    
        