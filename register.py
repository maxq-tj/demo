from django.shortcuts import redirect, render
from pApp.models import user


def Register(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        user.objects.create(
            email = email,
            password = password
        )

        #messages.success(request,"SaveData")

        return redirect("/")
    else:
        return render(request,"auth/Register.html")
