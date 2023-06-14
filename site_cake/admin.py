from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_cooker', 'is_customer')
    list_filter = ('is_staff', 'is_cooker', 'is_customer')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name', 'email')}),
        ('Доступы', {'fields': ('is_staff', 'is_cooker', 'is_customer')}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('id',)


admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city')


@admin.register(CookerRating)
class CookerRatingAdmin(admin.ModelAdmin):
    list_display = ('cooker', 'mark')


@admin.register(CookerPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ('status',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_name')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Filling)
class FillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'price')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'user')
    list_filter = ('status',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'created_on')
    list_filter = ('status',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'filling', 'created_on')
    ordering = ('created_on',)


@admin.register(FavoritePost)
class FavoritePostAdmin(admin.ModelAdmin):
    list_display = ("user", "post")


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cooker', 'created_on')
    ordering = ('created_on',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product', 'filling']


class UserOrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'cooker', 'delivery', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(UserOrder, UserOrderAdmin)
