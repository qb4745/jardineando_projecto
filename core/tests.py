from django.test import TestCase, Client
from django.urls import reverse
from django.views.generic import TemplateView
import random
import string

from core.forms import DonacionForm
from unittest.mock import patch

from core.models import Item

from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from core.models import Order
from django.utils import timezone
from django.contrib.auth import get_user_model  # Importa get_user_model


class HomeViewTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.url = reverse(
            "core:core-home"
        )
    def test_home_view_template(self):
        respuesta = self.cliente.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/home.html")
        self.assertIsInstance(respuesta.context["view"], TemplateView)

    def test_home_view_uses_correct_template(self):
        respuesta = self.cliente.get(self.url)
        self.assertTemplateUsed(respuesta, "core/home.html")
        self.assertTemplateNotUsed(
            respuesta, "wrong_template.html"
        )

def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))


class CreateRefCodeTest(TestCase):
    def test_ref_code_length(self):
        ref_code = create_ref_code()
        self.assertEqual(
            len(ref_code), 20, "El código de referencia debería tener una longitud de 20 caracteres"
        )

    def test_ref_code_characters(self):
        ref_code = create_ref_code()
        allowed_characters = string.ascii_lowercase + string.digits
        self.assertTrue(
            all(char in allowed_characters for char in ref_code),
            "El código de referencia solo debe contener letras minúsculas y dígitos",
        )


class NosotrosViewTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.url = reverse("core:core-nosotros")
        self.valid_rut = "13912058-2"  # Reemplázalo con un RUT chileno válido
        self.valid_data = {
            "nombre": "John",
            "apellido": "Doe",
            "correo": "john@example.com",
            "monto": 100,
            "codigo_pais": "+56",
            "telefono": 123456789,
            "rut": self.valid_rut,
            "rut_cifrado": "valid_cifrado_value",
            "rut_bcrypt": "valid_bcrypt_value",
        }

    @patch("core.models.rut_chile.is_valid_rut", return_value=True)
    def test_nosotros_view_form_submission(self, mock_is_valid_rut):
        respuesta = self.cliente.post(self.url, data=self.valid_data, follow=True)
        self.assertEqual(
            respuesta.status_code, 200
        )  # Asegurándose de que la redirección (estatus 302) sea seguida

        mock_is_valid_rut.assert_called_once_with(self.valid_rut)

    def test_nosotros_view_template(self):
        respuesta = self.cliente.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/nosotros.html")
        self.assertIsInstance(respuesta.context["form"], DonacionForm)


class CategoryItemListViewTest(TestCase):
    def setUp(self):
        # Crea algunos elementos de muestra para las pruebas
        self.item1 = Item.objects.create(
            title="Item 1",
            price=10.0,
            discount_price=8.0,
            category="A",
            slug="item-1",
            description="Descripción para el ítem 1",
        )
        self.item2 = Item.objects.create(
            title="Item 2",
            price=15.0,
            category="B",
            slug="item-2",
            description="Descripción para el ítem 2",
        )

        self.cliente = Client()
        self.url = reverse("core:core-products-category")

    def test_category_item_list_view_with_valid_category(self):
        respuesta = self.cliente.get(self.url, {"category": "A"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/products_category.html")
        self.assertContains(respuesta, "Item 1")
        self.assertNotContains(respuesta, "Item 2")

    def test_category_item_list_view_with_invalid_category(self):
        respuesta = self.cliente.get(self.url, {"category": "C"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/products_category.html")
        self.assertNotContains(respuesta, "Item 1")
        self.assertNotContains(respuesta, "Item 2")

    def test_category_item_list_view_with_search_query(self):
        respuesta = self.cliente.get(self.url, {"search": "Item 1"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/products_category.html")
        self.assertContains(respuesta, "Item 1")
        self.assertNotContains(respuesta, "Item 2")

    def test_category_item_list_view_with_invalid_search_query(self):
        respuesta = self.cliente.get(self.url, {"search": "Elemento no existente"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/products_category.html")
        self.assertNotContains(respuesta, "Item 1")
        self.assertNotContains(respuesta, "Item 2")


class ProfileViewTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.url = reverse("core:core-profile")
        self.usuario = User.objects.create_user(username="testuser", password="testpass")
        self.correo = EmailAddress.objects.create(
            user=self.usuario, email=self.usuario.email, verified=True
        )
        self.cliente.login(username="testuser", password="testpass")

    def test_profile_view_authenticated_user(self):
        # Crea una orden de muestra para el usuario autenticado
        fecha_pedido = timezone.now()
        orden = Order.objects.create(
            user=self.usuario, ordered=True, ordered_date=fecha_pedido
        )

        respuesta = self.cliente.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/profile.html")
        self.assertIn("orders", respuesta.context)
        self.assertEqual(list(respuesta.context["orders"]), [orden])

    def test_profile_view_unauthenticated_user(self):
        # Cierra la sesión del usuario para simular una solicitud no autenticada
        self.cliente.logout()

        respuesta = self.cliente.get(self.url)
        self.assertEqual(respuesta.status_code, 302)  # Redirige a la página de inicio de sesión
        self.assertRedirects(respuesta, f"{reverse('account_login')}?next={self.url}")


class ItemDetailViewTest(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.item = Item.objects.create(
            title="Ítem de Prueba",
            description="Descripción de prueba",
            price=100.0,
            slug="item-de-prueba",  # Establece un slug válido aquí
        )
        self.url = reverse("core:core-product", kwargs={"slug": self.item.slug})

    def test_item_detail_view(self):
        respuesta = self.cliente.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/product.html")
        self.assertEqual(respuesta.context["object"], self.item)

    def test_item_detail_view_random_products(self):
        # Crea elementos adicionales para las pruebas
        for _ in range(10):
            Item.objects.create(
                title="Ítem Aleatorio",
                description="Descripción aleatoria",
                price=50.0,
                slug="item-aleatorio",  # Establece un slug válido para cada ítem
            )

        respuesta = self.cliente.get(self.url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "core/product.html")

        # Comprueba si el ítem actual está en el contexto
        self.assertEqual(respuesta.context["object"], self.item)

        # Comprueba si hay 5 productos aleatorios en el contexto
        productos_aleatorios = respuesta.context.get("random_products")
        self.assertIsNotNone(productos_aleatorios)
        self.assertEqual(productos_aleatorios.count(), 5)

        # Comprueba si el ítem actual no está en la lista de productos aleatorios
        self.assertNotIn(self.item, productos_aleatorios)
        self.assertEqual(productos_aleatorios.count(), 5)
