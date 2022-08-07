from django.forms import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test default category'),
            author=self.make_author(username='newuser'),
            title = 'Recipe Title',
            description = 'Recipe description',
            slug = 'recipe-slug-for-no-defaults',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'Porções',
            preparation_step = 'Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
 
    @parameterized.expand([
            ('title', 65),
            ('description', 166),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_field_max_length(self, field, max_length):

        setattr(self.recipe, field, 'a' * (max_length + 2))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() 

    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_step_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testint Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testint Representation')

