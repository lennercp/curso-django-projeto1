from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


# @pytest.mark.functional_test
class RecipeHomePageFuncionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_whitout_recipers_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Sem receitas encontrada', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what i need'

        recipes[0].title = title_needed
        recipes[0].save()

        #User open the page
        self.browser.get(self.live_server_url)

        #See a find field with 'Search for a recipe' 
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for a recipe"]')

        #Clicks in this input and write a find term
        # "Recipe title 1" for find recipe with this title
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)


        self.assertIn(
            title_needed, 
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
            )
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        recipes = self.make_recipe_in_batch()

        #User open the page
        self.browser.get(self.live_server_url)

        #see a pagination and click in page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        #see what more 2 recipes in the page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )