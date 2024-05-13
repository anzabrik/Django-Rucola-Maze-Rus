from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("ingredients", views.Ingredients.as_view(), name="ingredients"),
    path("ingredients/new", views.IngredientNew.as_view(), name="ingredient_new"),
    path(
        "ingredients/<int:pk>/edit",
        views.IngredientUpdate.as_view(),
        name="ingredient_edit",
    ),
    path(
        "ingredients/<int:pk>/delete",
        views.IngredientDelete.as_view(),
        name="ingredient_delete",
    ),
    path("menu_items", views.MenuItems.as_view(), name="menu_items"),
    path("menu_items/new", views.MenuItemNew.as_view(), name="menu_item_new"),
    path(
        "menu_items/<int:pk>/edit",
        views.MenuItemUpdate.as_view(),
        name="menu_item_edit",
    ),
    path(
        "menu_items/<int:pk>/delete",
        views.MenuItemDelete.as_view(),
        name="menu_item_delete",
    ),
    path(
        "recipe_requirements",
        views.RecipeRequirements.as_view(),
        name="recipe_requirements",
    ),
    path(
        "recipe_requirements/new",
        views.RecipeRequirementNew.as_view(),
        name="recipe_requirement_new",
    ),
    path(
        "recipe_requirements/<int:pk>/edit",
        views.RecipeRequirementUpdate.as_view(),
        name="recipe_requirement_edit",
    ),
    path(
        "recipe_requirements/<int:pk>/delete",
        views.RecipeRequirementDelete.as_view(),
        name="recipe_requirement_delete",
    ),
    path(
        "purchases",
        views.Purchases.as_view(),
        name="purchases",
    ),
    path(
        "purchases/new",
        views.PurchaseNew.as_view(),
        name="purchase_new",
    ),
    path(
        "purchases/<int:pk>/edit",
        views.PurchaseUpdate.as_view(),
        name="purchase_edit",
    ),
    path(
        "purchases/<int:pk>/delete",
        views.PurchaseDelete.as_view(),
        name="purchase_delete",
    ),
]
