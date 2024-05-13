from django.shortcuts import render, redirect

from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm
from .models import User, Ingredient, MenuItem, RecipeRequirement, Purchase
from django.db.models import Sum
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse("home"))
        return render(
            request,
            "inventory/login.html",
            {"message": "Пароль неверный или логин не существует"},
        )
    return render(request, "inventory/login.html")


def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        email = request.POST["email"]
        if password != confirmation:
            return render(
                request,
                "inventory/sign_up.html",
                {"message": "Пароль и подтверждение пароля должны совпадать"},
            )
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(
                request,
                "inventory/sign_up.html",
                {"message": "Это имя пользователя уже занято"},
            )
        login(request, user)
        return redirect(reverse("home"))
    return render(request, "inventory/sign_up.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("login"))


@login_required
def home(request):
    revenue = Purchase.objects.aggregate(s=Sum("menu_item__price"))

    # Total cost of all purchases (sum of cost of all ingredients used)
    cost_of_ingredients = 0
    for p in Purchase.objects.all():
        for rr in p.menu_item.reciperequirement_set.all():
            cost_of_ingredients += rr.ingredient.unit_price * rr.quantity_required
    profit = revenue["s"] - cost_of_ingredients
    return render(
        request,
        "inventory/home.html",
        {
            "revenue": revenue["s"],
            "cost_of_ingredients": cost_of_ingredients,
            "profit": profit,
        },
    )


# Ingredients: new, list, edit, delete
class IngredientNew(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_new.html"
    form_class = IngredientForm


class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_edit.html"
    form_class = IngredientForm


class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete.html"
    success_url = reverse_lazy("ingredients")


class Ingredients(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredients.html"


# MenuItem: new, list, edit, delete
class MenuItemNew(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menu_item_new.html"
    form_class = MenuItemForm


class MenuItemUpdate(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "inventory/menu_item_edit.html"
    form_class = MenuItemForm


class MenuItemDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    success_url = reverse_lazy("menu_items")
    template_name = "inventory/menu_item_delete.html"


class MenuItems(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu_items.html"
    available_menu_items_titles = []
    available_menu_items_titles = [
        m_i.title for m_i in MenuItem.objects.all() if m_i.is_available()
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_menu_items_titles"] = self.available_menu_items_titles
        return context


# RecipeRequirement: new, list, edit, delete


class RecipeRequirementNew(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirement_new.html"
    form_class = RecipeRequirementForm


class RecipeRequirementUpdate(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirement_edit.html"
    form_class = RecipeRequirementForm


class RecipeRequirementDelete(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    success_url = reverse_lazy("recipe_requirements")
    template_name = "inventory/recipe_requirement_delete.html"


class RecipeRequirements(LoginRequiredMixin, ListView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirements.html"


# Purchase: new, list, edit, delete

class PurchaseNew(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = "inventory/purchase_new.html"
    form_class = PurchaseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["available_menu_items"] = [
            mi for mi in MenuItem.objects.all() if mi.is_available()
        ]
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            menu_item_id = request.POST["menu_item"]
            menu_item = MenuItem.objects.get(pk=menu_item_id)
            # Substract the required quantity from each of the Ingredients
            for mirr in menu_item.reciperequirement_set.all():
                mirr.ingredient.quantity_available -= mirr.quantity_required
                mirr.ingredient.save()

            # Record the purchase
            purchase = Purchase(menu_item=menu_item)
            purchase.save()
            return redirect(reverse("purchases"))


class PurchaseUpdate(LoginRequiredMixin, UpdateView):
    model = Purchase
    template_name = "inventory/purchase_edit.html"
    form_class = PurchaseForm


class PurchaseDelete(LoginRequiredMixin, DeleteView):
    model = Purchase
    success_url = reverse_lazy("purchases")
    template_name = "inventory/purchase_delete.html"


class Purchases(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchases.html"
