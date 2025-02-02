from django.shortcuts import render
from pApp.models import user


def showProfile(request):
      all_user = user.objects.all()
      return render(request, 'showProfile.html', {'all_user': all_user})