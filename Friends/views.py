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
        user_object = Account.objects.get(pk=display_name_from_form)
        user_object_is_valid = False
        if display_name_from_form != str(request.user):
            if user_object:
                user_object_is_valid = True
        if user_object_is_valid:
            Friend.objects.add_friend(
                request.user,
                user_object,
                message=f'{request.user} sent you a friend request'
            )
            return HttpResponse("Friend Request sent")
        else:
            return HttpResponse("User was not located")
    else:
        form = friendsearch_form()
        return render(request, 'Friends/friendsearch.html', {'form': form})
