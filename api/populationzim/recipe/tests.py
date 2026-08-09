from django.test import TestCase
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from geo.models import Recipe

from recipe.serializers import RecipeSerializer,RecipeDetailSerializer


RECIPES_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    """Create and return a recipe detail URL"""

    return reverse("recipe:recipe-detail", args=[recipe_id])

def create_recipe(user,**params):
    """Create & return a sample recipe"""

    defaults = { "title": "Rice Dovi",
                 "time_minutes": 13,
                 "price": Decimal("7.5"),
                 "description": "Mirairo yekubika rice rine dovi",
                 "link": "http://ravira.com/rice-dovi.pdf" }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user,**defaults)

    return recipe

def create_user(user_data):
    return get_user_model().objects.create_user(**user_data)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUP(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call api"""

        response = self.client.get(RECIPES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        user_data = { "email": "test-recipe@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Rhys Webb" }

        self.user = create_user(user_data)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieving list of recipes"""

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)
        
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes,many=True)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)

    def test_list_only_recipes_belonging_to_user(self):
        """Test that list of recipes returned contains only recipes owned by the currently logged in (authenticated) user"""
        
        user_data = { "email": "test-recipe1@ravira.com",
                      "password": "raviraindezvenyu",
                      "name": "Sebastian Negri" }

        other_user = get_user_model().objects.create_user(**user_data)
        
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many=True)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail"""
        
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        response = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(response.data,serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe using the endpoint successful"""

        recipe_data = { "title": "Rice Dovi",
                        "time_minutes": 13,
                        "price": Decimal("7.5"),
                        "description": "Mirairo yekubika rice rine dovi",
                        "link": "http://ravira.com/rice-dovi.pdf" }
        
        response = self.client.post(RECIPES_URL,recipe_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        recipe = Recipe.objects.get(id=response.data["id"])
        for k,v in recipe_data.items():
            self.assertEqual(getattr(recipe,k),v)
        self.assertEqual(recipe.user,self.user)

    def test_partial_recipe_update(self):
        """Test partial update of a recipe"""

        recipe_details = { "link": "https://ravira.com/mirairo.pdf",
                           "title": "Miraira ye Haifiridzi" }

        recipe = create_recipe(self.user,**recipe_details)
       
        updated_recipe_details = { "title": "Mirairo ye Haifirizdiii" }
        url = detail_url(recipe.id)
        response = self.client.patch(url,updated_recipe_details)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title,updated_recipe_details["title"])
        self.assertEqual(recipe.link,recipe_details["link"])
        self.assertEqual(recipe.user,self.user)
    
    def test_full_recipe_update(self):
        """Test full update of a recipe"""

        init_recipe_details = { "link": "https://ravira.com/mirairo.pdf",
                                "title": "Miraira ye Haifiridzi",
                                "description": "Unobika sei sadza nemurivo",
                                "time_minutes": 8,
                                "price": Decimal("9.1") }

        init_recipe = create_recipe(self.user,**init_recipe_details)
        
        updated_recipe_details = { "link": "https://ravira.com/haifiridzi.pdf",
                                   "title": "Mirairo ye sadza nemurivo",
                                   "description": "Unobika sei haifiridzi",
                                   "time_minutes": 9,
                                   "price": Decimal("8.1") }

        updated_recipe = create_recipe(self.user,**updated_recipe_details)
        
        url = detail_url(init_recipe.id)
        response = self.client.put(url,updated_recipe_details)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        init_recipe.refresh_from_db()
        self.assertEqual(init_recipe.price,updated_recipe_details["price"])
        self.assertEqual(init_recipe.description,updated_recipe_details["description"])
        self.assertEqual(init_recipe.time_minutes,updated_recipe_details["time_minutes"])
        self.assertEqual(init_recipe.title,updated_recipe_details["title"])
        self.assertEqual(init_recipe.link,updated_recipe_details["link"])
        self.assertEqual(init_recipe.user,self.user)

    def test_delete_recipe(self):
        """Test successful deletion of a recipe"""

        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
