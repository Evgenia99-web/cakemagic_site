from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.PostsPage, name='posts'),
    path('recipes/', views.RecipePage, name='recipes'),
    path('cart/', views.CartView, name='cart'),
    path('basket/add/product_<int:product_id>_filling_<int:filling_id>_count_<int:count>', views.basket_add, name='basket_add'),
    path('basket/delete/basket_<int:basket_id>', views.basket_remove, name='basket_delete'),
    path('posts/<int:id>/', views.post_detail, name='post_single'),
    path('posts/favorite_<int:id>/', views.UserFavoritePost, name='post_fav'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_single'),
    path('recipes/favorite_<int:id>/', views.UserFavoriteRecipe, name='recipe_fav'),
    path('cookers/', views.CookerListView, name='cookers'),
    path('cookers/<int:id>/', views.cooker_detail, name='cooker_single'),
    path('goods/<int:id>_cooker<int:cooker>/', views.good_detail, name='good_single'),
    path('success_order/', views.SuccessOrder, name='success_order'),
    path('order/<int:total_sum>', views.order_create, name='create_order'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profile/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.UpdateProfile, name='edit_profile'),

    path('profile_posts/', views.PostProfileListView, name='profile_posts'),
    path('profile_favorite_posts/', views.ProfileFavoritePosts, name='profile_fav_posts'),
    path('profile_posts/new/', views.CreatePostProfile, name='add_post'),
    path('profile_posts/<int:id>/', views.RetrievePostProfile, name='post_detail'),
    path('profile_posts/edit/<int:id>/', views.UpdatePostProfile, name='edit_post'),
    path('profile_posts/delete/<int:id>/', views.DeletePostProfile, name='delete_post'),
    path('profile_favorite_posts/delete/<int:id>/', views.delete_fav_post, name='delete_fav_post'),
    path('profile_favorite_posts/delete/all/', views.delete_fav_post_all, name='delete_fav_post_all'),

    path('profile_goods/', views.GoodProfileListView, name='profile_goods'),
    path('profile_goods/new/', views.CreateGoodProfile, name='add_good'),
    path('profile_goods/<int:id>/', views.RetrieveGoodProfile, name='good_detail'),
    path('profile_goods/edit/<int:id>/', views.UpdateGoodProfile, name='edit_good'),
    path('profile_goods/delete/<int:id>/', views.DeleteGoodProfile, name='delete_good'),

    path('profile_filling/new/', views.CreateFilProfile, name='add_filling'),

    path('profile_recipes/', views.RecipeProfileListView, name='profile_recipes'),
    path('profile_favorite_recipe/', views.ProfileFavoriteRecipe, name='profile_fav_recipes'),
    path('profile_recipes/new/', views.CreateRecipeProfile, name='add_recipe'),
    path('profile_recipes/<int:id>/', views.RetrieveRecipeProfile, name='recipe_detail'),
    path('profile_recipes/edit/<int:id>/', views.UpdateRecipeProfile, name='edit_recipe'),
    path('profile_recipes/delete/<int:id>/', views.DeleteRecipeProfile, name='delete_recipe'),
    path('profile_favorite_recipes/delete/<int:id>/', views.delete_fav_recipe, name='delete_fav_recipe'),
    path('profile_favorite_recipes/delete/all/', views.delete_fav_recipe_all, name='delete_fav_recipe_all'),

    path('profile_orders/', views.ProfileOrders, name='profile_orders'),
    path('profile_orders/edit/<int:id>', views.ChangeStatus, name='change_status'),
]