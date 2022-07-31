from django.forms import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_reciple_titles_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'b' * 66

        with self.assertRaises(ValidationError):
            self.recipe.full_clean() # AQ UI A VALIDAÇÃO OCORRE

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_field_max_length(self, field, max_length):

        setattr(self.recipe, field, (max_length + 0))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean() 
