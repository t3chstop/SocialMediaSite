from django import http
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from friendship.models import Friend, Follow, Block
from .forms import friendsearch_form
from accounts.models import Account


# Create your views here.
@login_required
def friendsearch_view(request):
    if request.method == 'POST':
        form = friendsearch_form(request.POST)
        display_name_from_form = form.data.get('display_name')
        user_object_exists = Account.objects.filter(display_name=display_name_from_form).exists()
        if user_object_exists:
            return HttpResponse('User was located')
        else:
            return HttpResponse('User was not located')
    else:
        form = friendsearch_form()
        return render(request, 'Friends/friendsearch.html', {'form': form})