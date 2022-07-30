from tkinter.font import names

from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def make_category(self, name='category'):
        return Category.objects.create(name=name)

    def make_author(self, 
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com'):
        
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(self, 
        category_data=None,
        author_data=None,
        title = 'Recipe Title',
        description = 'Recipe description',
        slug = 'recipe-slug',
        preparation_time = 10,
        preparation_time_unit = 'Minutos',
        servings = 5,
        servings_unit = 'Porções',
        preparation_step = 'Recipe Preparation Steps',
        preparation_step_is_html = False,
        is_published = True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time_unit=preparation_time_unit,
            preparation_time=preparation_time,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published
        )
