from django.forms import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_reciple_titles_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'b' * 66

        with self.assertRaises(ValidationError):
            self.recipe.full_clean() # AQUI A VALIDAÇÃO OCORRE

