from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib import messages

from .models import User, Listing, Category, Comment
from .forms import NewListingForm, BidForm, CommentForm


def index(request):
    print(Listing.objects.filter(active=True))
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
# Добавить новый товар
def newlisting(request):

    if request.method == "POST":
        form = NewListingForm(request.POST)

        if form.is_valid():
            form.instance.author = request.user
            new_listing = form.save()
            return HttpResponseRedirect(reverse("listing", args=(new_listing.pk,)))

    else:
        form = NewListingForm()
    
    return render(request, "auctions/newlisting.html", {
        "form": form
    })

# Переход на страницу товара
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.all()
    total_comments = comments.count()

    if request.user.is_authenticated:
        is_in_watchlist = listing.is_in_watchlist(request.user)
    else:
        is_in_watchlist = False
    
    return render (request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(),
        "comment_form": CommentForm(),
        "comments": comments,
        "total_comments": total_comments,
        "is_in_watchlist": is_in_watchlist,
        "user": request.user
    })

# Добавить ставку
@login_required(login_url='login')
def add_bid(request, listing_id):
    if request_method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        form = BidForm(request.POST)

        if form.is_valide():
            form.instance.user = request.user
            form.instance.item = listing

            if form.instance.amount > listing.current_price():
                form.sava()
                messages.success(request, 'Ставка успешно сделана.')
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                messages.error(request, 'Ставка должна быть больше текущей ставки')
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
# Добавить Коментарий
@login_required(login_url='login')
def add_comment(request, listing_id):
    if request_method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        form = CommentForm(request.POST)

        if form.is_valide():
            form.instance.user = request.user
            form.instance.item = listing
            form.save()
            message.success(request, 'Коментарий успешно добавлен.')
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# страница с категориями
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by('name'),
    })

# список товаров категории
def category(request, category_id):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=category_id),
        "listings": Listing.objects.filter(active=True, category=category_id)
    })


