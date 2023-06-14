from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, username=None, is_cooker=False,
                    is_customer=False):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_cooker=is_cooker,
            is_customer=is_customer
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, first_name=None, last_name=None, username=None, is_cooker=False,
                         is_customer=False):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_cooker=is_cooker,
            is_customer=is_customer
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_cooker = False
        user.is_customer = False
        user.set_password(password)
        user.save(using=self._db)


class User(AbstractUser):
    first_name = models.CharField(max_length=60, null=True)
    last_name = models.CharField(max_length=60, null=True)
    email = models.EmailField(max_length=60, unique=True, blank=True, null=True, default=None)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    is_cooker = models.BooleanField('Статус кондитера', default=False)
    is_customer = models.BooleanField('Статус заказчика', default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default='Россия')
    city = models.CharField(max_length=100, default='Москва')
    phone = models.CharField(max_length=11, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(default='default_ava.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} профиль'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CookerRating(models.Model):
    cooker = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(default=5)

    def __str__(self):
        return f'{self.cooker.username} - {self.mark}'

    class Meta:
        verbose_name = 'Оценка кондитера'
        verbose_name_plural = 'Оценки кондитеров'


class CookerPost(models.Model):
    POST_STATUS = [
        ('1', 'Черновик'),
        ('2', 'Опубликовано'),
        ('3', 'На модерации'),
    ]
    cooker = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    image_post = models.ImageField(upload_to='post_pics')
    video_url = models.URLField(blank=True, verbose_name="URL видео", help_text="URL видео")
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=POST_STATUS, default='1', max_length=1)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['id']

    def save(self):
        super().save()

        img = Image.open(self.image_post.path)

        if img.height > 990 or img.width > 790:
            output_size = (990, 790)
            img.thumbnail(output_size)
            img.save(self.image_post.path)


class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.cat_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Type(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.type_name}'

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Filling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(default='default_fil.jpg', upload_to='fillings_pics')

    def __str__(self):
        return f'Начинка: {self.name}'

    class Meta:
        verbose_name = 'Начинка'
        verbose_name_plural = 'Начинки'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 250 or img.width > 110:
            output_size = (250, 110)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Product(models.Model):
    PRODUCT_STATUS = [
        ('1', 'Черновик'),
        ('2', 'Опубликовано'),
        ('3', 'На модерации'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image_good = models.ImageField(default='default_good.png', upload_to='profile_goods')
    status = models.CharField(choices=PRODUCT_STATUS, default='1', max_length=1)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Recipe(models.Model):
    RECIPE_STATUS = [
        ('1', 'Черновик'),
        ('2', 'Опубликовано'),
        ('3', 'На модерации'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    video_url = models.CharField(null=True, blank=True, max_length=400, verbose_name="Ссылка на видео",
                                 help_text="Ссылка на видеорецепт (YouTube)")
    doc_recipe = models.FileField(null=True, blank=True, upload_to='recipe_doc/')
    created_on = models.DateTimeField(auto_now_add=True)
    image_recipe = models.ImageField(default='default_recipe.jpg', upload_to='recipe_pics')
    status = models.CharField(choices=RECIPE_STATUS, default='1', max_length=1)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    filling = models.ForeignKey(Filling, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name} | Начинка: {self.filling.name}'

    def sum(self):
        return self.filling.price * self.quantity

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class FavoritePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(CookerPost, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Любимая публикация'
        verbose_name_plural = 'Любимые публикации'

    def __str__(self):
        return str(self.post)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'

    def __str__(self):
        return str(self.recipe)


class Feedback(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    cooker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cooker")
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.customer.username)


class UserOrder(models.Model):
    ORDER_STATUS = [
        ('1', 'Обрабатывается'),
        ('2', 'Отклонен'),
        ('3', 'Принят'),
        ('4', 'В работе')
    ]
    DELIVERY_STATUS = [
        ('1', 'Доставка'),
        ('2', 'Самовывоз')
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer2")
    cooker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cooker2")
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery = models.CharField(choices=DELIVERY_STATUS, default='1', max_length=1)
    status = models.CharField(choices=ORDER_STATUS, default='1', max_length=1)


    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    filling = models.ForeignKey(Filling, on_delete=models.CASCADE, related_name='filling_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity