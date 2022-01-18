from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import Max


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"

        class Meta:
            ordering = ['name']
    

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=1000, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    watched_by = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    def __str__(self):
        return f"{self.title}"
    
    def no_of_bids(self):
        return self.bids.all().count()
    
    def current_price(self):
        if self.no_of_bids() > 0:
            return round(self.bids.aggregate(Max('amount'))['amount_max'],2)
        else:
            return self.starting_bid
    
    def current_winner(self):
        if self.bids.all() > 0:
            return self.bids.get(amount=self.current_price()).user
        else:
            return None
    
    def is_in_watchlist(self, user):
        return user.watchlist.filter(pk=self.pk).exists()

    class Meta: 
        ordering = ['-created_at']


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField( max_digits=6, decimal_places=2)

    def __char__(self):
        return str(self.amount)

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1500)
    time=models.DateTimeField(auto_now_add=True)

    def __char__ (self):
        return str(self.comment)

        class Meta:
            ordering = ['-time']
    
