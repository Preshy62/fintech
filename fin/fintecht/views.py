from django.shortcuts import render

# Create your views here.




def index(request):
    return render(request, "index.html")


# login view


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        google_code = request.POST.get("google_code")

        user = authenticate(request, username=username, password=password)
        
        if user:
            if user.require_google_auth:
                if not google_code:
                    messages.error(request, "Google Authentication code is required.")
                    return render(request, "login.html")

                if not user.verify_google_code(google_code):
                    messages.error(request, "Invalid Google Authentication code.")
                    return render(request, "login.html")

            login(request, user)
            return redirect("dashboard")  # Redirect to your home page

        messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")



import pyotp
import qrcode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def enable_google_auth(request):
    user = request.user

    if not user.google_auth_secret:
        user.generate_google_secret()
    
    totp = pyotp.TOTP(user.google_auth_secret)
    qr_url = totp.provisioning_uri(user.username, issuer_name="MyDjangoApp")

    # Generate QR code
    qr = qrcode.make(qr_url)
    qr_path = f"media/qrcodes/{user.username}.png"
    qr.save(qr_path)

    if request.method == "POST":
        code = request.POST["code"]
        if user.verify_google_code(code):
            user.require_google_auth = True
            user.save()
            return redirect("dashboard")
        else:
            return render(request, "enable_google_auth.html", {"error": "Invalid code"})

    return render(request, "enable_google_auth.html", {"qr_code": qr_path})


                            #    799999999


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically
            return redirect('index')  # Redirect to home page after signup
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
