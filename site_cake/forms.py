from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_cooker', 'is_customer', 'password1', 'password2']
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Введите имя",
                    "label": "Имя",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Введите фамилию",
                    "label": "Фамилия",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Введите логин",
                    "label": "Логин",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "required": True,
                    "placeholder": "Введите email",
                    "label": "Email",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Имя"
        self.fields['last_name'].label = "Фамилия"
        self.fields['username'].label = "Логин"
        self.fields['is_cooker'].label = "Вы кондитер"
        self.fields['is_customer'].label = "Вы заказчик"

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None


class AddCookerPost(forms.ModelForm):
    class Meta:
        model = CookerPost
        fields = ['title', 'video_url', 'content', 'image_post', 'status']

    def __init__(self, *args, **kwargs):
        super(AddCookerPost, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Заголовок"
        self.fields['video_url'].label = "Ссылка на видео"
        self.fields['video_url'].help_text = None
        self.fields['content'].label = "Текст публикации"
        self.fields['image_post'].label = "Изображение публикации"
        self.fields['status'].label = "Статус публикации"


class AddCookerGood(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'type', 'description', 'image_good', 'status']

    def __init__(self, *args, **kwargs):
        super(AddCookerGood, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Название товара"
        self.fields['category'].label = "Категория товара"
        self.fields['type'].label = "Тип товара"
        self.fields['description'].label = "Описание товара"
        self.fields['image_good'].label = "Изображение товара"
        self.fields['status'].label = "Статус товара"


class AddCookerFilling(forms.ModelForm):
    class Meta:
        model = Filling
        fields = ['name', 'type', 'description', 'image', 'price']

    def __init__(self, *args, **kwargs):
        super(AddCookerFilling, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Название начинки"
        self.fields['type'].label = "Тип товара начинки"
        self.fields['description'].label = "Описание начинки (состав)"
        self.fields['image'].label = "Изображение начинки"
        self.fields['price'].label = "Цена начинки"
        self.fields['price'].help_text = "Цена начинки указывается за 1кг или, например, за 2 шт капкейков"


class AddCookerRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'category', 'type', 'status', 'doc_recipe', 'image_recipe']

    def __init__(self, *args, **kwargs):
        super(AddCookerRecipe, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Название рецепта"
        self.fields['type'].label = "Тип рецепта"
        self.fields['category'].label = "Категория рецепта"
        self.fields['image_recipe'].label = "Изображение рецепта"
        self.fields['status'].label = "Статус"


class CookerFilter(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['type', 'category']

    def __init__(self, *args, **kwargs):
        super(CookerFilter, self).__init__(*args, **kwargs)
        self.fields['type'].label = "Выберете тип"
        self.fields['category'].label = "Выберете категорию"


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
         super(UserUpdateForm, self).__init__(*args, **kwargs)
         self.fields['username'].label = "Логин"
         self.fields['first_name'].label = "Имя"
         self.fields['last_name'].label = "Фамилия"


class ProfileCookerUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'city', 'phone', 'description', 'image']

    def __init__(self, *args, **kwargs):
         super(ProfileCookerUpdateForm, self).__init__(*args, **kwargs)
         self.fields['country'].label = "Страна"
         self.fields['city'].label = "Город"
         self.fields['phone'].label = "Телефон"
         self.fields['description'].label = "Описание профиля"
         self.fields['image'].label = "Изображение профиля"


class ProfileCustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'city', 'phone', 'image']

    def __init__(self, *args, **kwargs):
         super(ProfileCustomerUpdateForm, self).__init__(*args, **kwargs)
         self.fields['country'].label = "Страна"
         self.fields['city'].label = "Город"
         self.fields['phone'].label = "Телефон"
         self.fields['image'].label = "Изображение профиля"


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = UserOrder
        fields = ['city', 'delivery', 'phone', 'address', 'email']
        date_need = forms.DateField(label='Дата праздника', required=True,
                                   widget=MyDateInput({
                                       'class': 'form-control'
                                   }))

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        self.fields['city'].label = "Город заказа"
        self.fields['delivery'].label = "Способ получения"
        self.fields['phone'].label = "Телефон"
        self.fields['address'].label = "Адрес доставки"
        self.fields['email'].label = "Почта"


class ChangeStatusOrder(forms.ModelForm):
    class Meta:
        model = UserOrder
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(ChangeStatusOrder, self).__init__(*args, **kwargs)
        self.fields['status'].label = "Статус заказа"