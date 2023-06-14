from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.http import FileResponse, Http404
from django.core.paginator import Paginator
from .forms import *
from .models import *


# Create your views here.
def home(request):
    post_list = CookerPost.objects.order_by('?')[:6]
    recipe_list = Recipe.objects.order_by('?')[:6]
    feedbacks = Feedback.objects.order_by('?')[:5]
    return render(request, 'main_page.html', {'post_list': post_list, 'recipe_list': recipe_list, 'feedbacks':feedbacks})


def PostsPage(request):
    post_list = CookerPost.objects.order_by('?')
    paginator = Paginator(post_list, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts.html', {'post_list': post_list, 'page_obj': page_obj,})


def RecipePage(request):
    recipe_list = Recipe.objects.order_by('?')
    paginator = Paginator(recipe_list, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recipies.html', {'recipe_list': recipe_list, 'page_obj': page_obj,})


def CookerListView(request):
    cooker_list = User.objects.filter(is_cooker=True)
    cooker_top = User.objects.filter(is_cooker=True)[:3]
    paginator = Paginator(cooker_list, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        city = request.POST['city']
        if User.objects.filter(userprofile__city=city, is_cooker=True).count() > 0:
            page_obj = User.objects.filter(userprofile__city=city, is_cooker=True)
        else:
            messages.error(request, f'К сожалению, кондитеров из города {city} еще нет.')

    return render(request, 'cookers.html', {'cooker_list': cooker_list, 'cooker_top': cooker_top, 'page_obj': page_obj})


def about(request):
    return render(request, 'about.html')


def cooker_detail(request, id):
    cooker = User.objects.get(pk=id)
    filter_form = CookerFilter()
    goods_list = Product.objects.filter(user=id).order_by('-id')
    posts_list = CookerPost.objects.filter(cooker=id).order_by('-id')
    recipes_list = Recipe.objects.filter(user=id).order_by('-id')
    feed_list = Feedback.objects.filter(cooker=id).order_by('-id')

    paginator1 = Paginator(goods_list, 9)
    page_number1 = request.GET.get('page')
    page_obj1 = paginator1.get_page(page_number1)

    paginator2 = Paginator(posts_list, 9)
    page_number2 = request.GET.get('page')
    page_obj2 = paginator2.get_page(page_number2)

    paginator3 = Paginator(recipes_list, 9)
    page_number3 = request.GET.get('page')
    page_obj3 = paginator3.get_page(page_number3)

    paginator4 = Paginator(feed_list, 6)
    page_number4 = request.GET.get('page')
    page_obj4 = paginator4.get_page(page_number4)

    if not feed_list:
        messages.success(request, f'У кондитера еще нет отзывов. Закажите и станьте первым.')

    context = {
        'cooker_info': cooker,
        'filter': filter_form,
        'page_obj1': page_obj1,
        'page_obj2': page_obj2,
        'page_obj3': page_obj3,
        'page_obj4': page_obj4
    }
    return render(request, 'cooker_detail.html', context)


def good_detail(request, id, cooker):
    good = Product.objects.get(pk=id)
    filling_list = Filling.objects.filter(user=cooker, type=good.type)
    weight = 0
    fil_id = 0
    fil_name = ''
    total_price = 0

    if request.method == 'POST':
        weight = request.POST.get('weight')
        fil_id = request.POST.get('fil_price')
        fil = Filling.objects.get(pk=fil_id)
        price = fil.price
        fil_name = fil.name
        fil_id = fil.pk
        total_price = int(weight) * int(price)

    context = {
        'good_info': good,
        'filling_list': filling_list,
        'total_price': total_price,
        'weight': weight,
        'fil_name': fil_name,
        'fil_id': fil_id
    }
    return render(request, 'good_detail.html', context)


def post_detail(request, id):
    post = CookerPost.objects.get(pk=id)

    if request.user:
        if not FavoritePost.objects.filter(post=id, user=request.user.id):
            fav = False
        else:
            fav = True

    return render(request, 'post_detail.html', {'post_info': post, 'fav': fav})


def recipe_detail(request, id):
    recipe = Recipe.objects.get(pk=id)

    if not FavoriteRecipe.objects.filter(recipe=id, user=request.user.id):
        fav = False
    else:
        fav = True

    return render(request, 'recipe_detail.html', {'recipe_info': recipe, 'fav': fav})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def CartView(request):
    basket = Basket.objects.filter(user=request.user)
    context = {
        'basket': basket
    }
    return render(request, 'cart.html', context)


@login_required
def basket_add(request, product_id, filling_id, count):
    product = Product.objects.get(pk=product_id)
    filling = Filling.objects.get(pk=filling_id)
    baskets = Basket.objects.filter(user=request.user, product=product, filling=filling)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, filling=filling, quantity=count)
    else:
        basket = baskets.first()
        basket.quantity = basket.quantity + count
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def profile(request):
    user_goods = Product.objects.filter(user=request.user).count()

    if request.user.is_customer:
        count_posts = FavoritePost.objects.filter(user=request.user).count()
        count_recipes = FavoriteRecipe.objects.filter(user=request.user).count()
        orders_custom = UserOrder.objects.filter(customer=request.user).count()
        feed_cust = Feedback.objects.filter(customer=request.user).count()
    else:
        count_posts = ''
        count_recipes = ''
        orders_custom = ''
        feed_cust = ''

    if request.user.is_cooker:
        marks = CookerRating.objects.filter(cooker=request.user)
        count_marks = CookerRating.objects.filter(cooker=request.user).count()
        raiting = sum(mark.mark for mark in marks)/count_marks
        orders_cooker = UserOrder.objects.filter(cooker=request.user).count()
        feed_cook = Feedback.objects.filter(cooker=request.user).count()
    else:
        raiting = ''
        orders_cooker = ''
        feed_cook = ''

    context = {
        'count_user_goods': user_goods,
        'raiting': raiting,
        'count_posts': count_posts,
        'count_recipes':count_recipes,
        'orders_custom':orders_custom,
        'orders_cooker':orders_cooker,
        'feed_cook': feed_cook ,
        'feed_cust': feed_cust

    }
    return render(request, 'profile/profile_main.html', context)


def PostProfileListView(request):
    logged_in_user_posts = CookerPost.objects.filter(cooker=request.user.id).order_by('-created_on')
    paginator = Paginator(logged_in_user_posts, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'profile/profile_posts.html', {'post_list': page_obj})


def CreatePostProfile(request):
    if request.method == 'POST':
        post_form = AddCookerPost(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.cooker = request.user
            post.created_on = timezone.now()
            post.updated_on = timezone.now()
            post.save()
            messages.success(request, f'Ваша публикация создана: можете вернуться ко всем записям.')
            redirect('profile_posts')
    else:
        post_form = AddCookerPost()

    return render(request, 'profile/profile_add_post.html', {'form': post_form, })


def RetrievePostProfile(request, id):
    post = CookerPost.objects.get(pk=id)
    return render(request, 'profile/profile_post_detail.html', {'post_info': post, })


def UpdatePostProfile(request, id):
    post = get_object_or_404(CookerPost, pk=id)
    if request.method == "POST":
        form = AddCookerPost(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.cooker = request.user
            post.updated_on = timezone.now()
            post.save()
            return redirect('profile_posts')
    else:
        form = AddCookerPost(instance=post)
    return render(request, 'profile/profile_post_edit.html', {'form': form})


def DeletePostProfile(request, id):
    post_to_delete = CookerPost.objects.get(pk=id)
    post_to_delete.delete()
    return redirect('profile_posts')


def GoodProfileListView(request):
    logged_in_user_goods = Product.objects.filter(user=request.user.id).order_by('-created_on')
    paginator = Paginator(logged_in_user_goods, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'profile/profile_goods.html', {'good_list': page_obj})


def CreateGoodProfile(request):
    if request.method == 'POST':
        good_form = AddCookerGood(request.POST, request.FILES)
        if good_form.is_valid():
            good = good_form.save(commit=False)
            good.user = request.user
            good.created_on = timezone.now()
            good.save()
            messages.success(request, f'Ваш товар создан: можете вернуться ко всем товарам.')
            redirect('profile_goods')
    else:
        good_form = AddCookerGood()

    return render(request, 'profile/profile_add_good.html', {'form': good_form, })


def RetrieveGoodProfile(request, id):
    good = Product.objects.get(pk=id)
    count_fil = Filling.objects.filter(user=request.user, type=good.type).count()
    filling_list = Filling.objects.filter(user=request.user, type=good.type)

    if count_fil == 0:
        messages.success(request, f'У вас пока нет подходящих начинок для этого товара. Вы можете их добавить здесь.')

    return render(request, 'profile/profile_good_detail.html', {'good_info': good, 'fil_list': filling_list, })


def UpdateGoodProfile(request, id):
    good = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        form_good = AddCookerGood(request.POST, instance=good)
        if form_good.is_valid():
            good = form_good.save(commit=False)
            good.cooker = request.user
            good.updated_on = timezone.now()
            good.save()
            return redirect('profile_goods')
    else:
        form_good = AddCookerGood(instance=good)
    return render(request, 'profile/profile_post_edit.html', {'form': form_good})


def DeleteGoodProfile(request, id):
    good_to_delete = Product.objects.get(pk=id)
    good_to_delete.delete()
    return redirect('profile_goods')


def CreateFilProfile(request):
    if request.method == 'POST':
        fil_form = AddCookerFilling(request.POST, request.FILES)
        if fil_form.is_valid():
            fil = fil_form.save(commit=False)
            fil.user = request.user
            fil.created_on = timezone.now()
            fil.save()
            messages.success(request, f'Ваша начинка создана: можете вернуться ко всем товарам.')
            redirect('profile_goods')
    else:
        fil_form = AddCookerFilling()

    return render(request, 'profile/profile_add_filing.html', {'form': fil_form, })


def RecipeProfileListView(request):
    logged_in_user_recipes = Recipe.objects.filter(user=request.user.id).order_by('-created_on')
    paginator = Paginator(logged_in_user_recipes, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'profile/profile_recipes.html', {'recipe_list': page_obj})


def CreateRecipeProfile(request):
    if request.method == 'POST':
        recipe_form = AddCookerRecipe(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.created_on = timezone.now()
            recipe.save()
            messages.success(request, f'Ваш рецепт создан: можете вернуться ко всем рецептам.')
            redirect('profile_goods')
    else:
        recipe_form = AddCookerRecipe()

    return render(request, 'profile/profile_add_recipe.html', {'form': recipe_form, })


def RetrieveRecipeProfile(request, id):
    recipe = Recipe.objects.get(pk=id)
    return render(request, 'profile/profile_recipe_detail.html', {'recipe_info': recipe, })


def DeleteRecipeProfile(request, id):
    recipe_to_delete = Recipe.objects.get(pk=id)
    recipe_to_delete.delete()
    return redirect('profile_goods')


def UpdateRecipeProfile(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if request.method == "POST":
        form_recipe = AddCookerRecipe(request.POST, instance=recipe)
        if form_recipe.is_valid():
            recipe = form_recipe.save(commit=False)
            recipe.cooker = request.user
            recipe.save()
            return redirect('profile_recipes')
    else:
        form_recipe = AddCookerRecipe(instance=recipe)
    return render(request, 'profile/profile_post_edit.html', {'form': form_recipe})


def UpdateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        cook_form = ProfileCookerUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        cust_form = ProfileCustomerUpdateForm(request.POST,
                                            request.FILES,
                                            instance=request.user.userprofile)
        if u_form.is_valid() and cook_form.is_valid():
            u_form.save()
            cook_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')
        elif u_form.is_valid() and cust_form.is_valid():
            u_form.save()
            cust_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        cook_form = ProfileCookerUpdateForm(instance=request.user.userprofile)
        cust_form = ProfileCustomerUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'cook_form': cook_form,
        'cust_form': cust_form
    }

    return render(request, 'profile/profile_edit.html', context)


def UserFavoritePost(request, id):
    current_post = CookerPost.objects.get(pk=id)
    if not FavoritePost.objects.filter(post=current_post):
        fav_post = FavoritePost(
            post=CookerPost.objects.get(pk=id),
            user=request.user,
        )
        fav_post.save()
    else:
        FavoritePost.objects.filter(post=current_post).delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def UserFavoriteRecipe(request, id):
    current_recipe = Recipe.objects.get(pk=id)
    if not FavoriteRecipe.objects.filter(recipe=current_recipe):
        fav_recipe = FavoriteRecipe(
            recipe=Recipe.objects.get(pk=id),
            user=request.user,
        )
        fav_recipe.save()
    else:
        FavoriteRecipe.objects.filter(recipe=current_recipe).delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def ProfileFavoritePosts(request):
    fav_posts = FavoritePost.objects.filter(user=request.user)

    if not fav_posts:
         messages.success(request, f'У вас еще нет любимых публикаций, добавьте их скорее.')

    return render(request, 'profile/profile_fav_posts.html', {'fav_posts': fav_posts, })


def ProfileFavoriteRecipe(request):
    fav_recipe = FavoriteRecipe.objects.filter(user=request.user)
    if not fav_recipe:
         messages.success(request, f'У вас еще нет любимых рецептов, добавьте их скорее.')

    return render(request, 'profile/profile_fav_recipes.html', {'fav_posts': fav_recipe, })


def delete_fav_post(request, id):
    FavoritePost.objects.filter(pk=id).delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def delete_fav_recipe(request, id):
    FavoriteRecipe.objects.filter(pk=id).delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def delete_fav_post_all(request):
    FavoritePost.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def delete_fav_recipe_all(request):
    FavoriteRecipe.objects.filter(user=request.user).delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def order_create(request, total_sum):
    basket = Basket.objects.filter(user=request.user)
    if request.method == 'POST':
        form_order = CreateOrderForm(request.POST)
        if form_order.is_valid():
            order = form_order.save(commit=False)
            order.customer = request.user
            order.created = timezone.now()
            order.updated = timezone.now()
            for item in basket:
                order.cooker = item.product.user
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         filling=item['filling'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            order.save()
            basket.clear()
            return render('success_order')
    else:
        form_order = CreateOrderForm()

    return render(request, 'order.html', {'baskets': basket, 'order_form': form_order, 'total_sum': total_sum})


@login_required
def SuccessOrder(request):
    return render(request, 'succses_order.html')


def ProfileOrders(request):
    if request.user.is_cooker:
        orders = UserOrder.objects.filter(cooker=request.user)
    else:
        orders = UserOrder.objects.filter(customer=request.user)

    return render(request, 'profile/profile_orders.html', {'orders': orders, })


def ChangeStatus(request, id):
    order = get_object_or_404(UserOrder, pk=id)
    if request.method == "POST":
        form_order = ChangeStatusOrder(request.POST, instance=order)
        if form_order.is_valid():
            order.save()
            return redirect('profile_orders')
    else:
        form_order = ChangeStatusOrder(instance=order)
    return render(request, 'profile/profile_change_status.html', {'form': form_order})