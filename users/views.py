from django.contrib.auth import user_logged_out
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from products.models import Product
from .forms import SignUpForm, UpdateProfileform
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.shortcuts import redirect, get_object_or_404
from .models import CustomUser, Saved
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class SignUpView(UserPassesTestMixin, View):

    def get(self, request):
        return render(request, "registration/signup.html", {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account is successfully created")
            return redirect('login')
        else:
            return render(request, "registration/signup.html", {'form': form})

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return False
        return True


def logout_view(request):
    products = Product.objects.all()
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", True):
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, "user"):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()
    return render(request, "index.html", {"products": products})


class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile.html', {'customuser': user})


class UpdateProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = UpdateProfileform(instance=request.user)
        return render(request, 'profile_update.html', {'form': form})

    def post(self, request):
        form = UpdateProfileform(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account is succesfully updated")
            return redirect("users:profile", request.user)
        return render(request, 'registration/signup.html', {'form': form})


class AddRemoveSavedView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        saved_product = Saved.objects.filter(author=request.user, product=product)
        if saved_product:
            saved_product.delete()
            messages.info(request, "Removed . ")
        else:
            Saved.objects.create(author=request.user, product=product)
            messages.info(request, "Saved !")
        return redirect(request.META.get("HTTP_REFERER"))


class SavedView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        saveds = Saved.objects.filter(author=request.user)
        return render(request, 'saveds.html', {'saveds': saveds})
 

class RecentlyViewedView(View):
    def get(self, request):
        if not "recently_viewed" in request.session:
            products = []
        else:
            r_viewed = request.session["recently_viewed"]
            products = Product.objects.filter(id__in=r_viewed)
            q = request.GET.get('q', '')
            if q:
                products = products.filter(title__icontains=q)
        return render(request, "recently_viewed.html", {'products': products})

