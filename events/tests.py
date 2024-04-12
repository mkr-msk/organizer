from django.test import TestCase
from events.models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Первый элемент списка'
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый элемент списка')
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')


class EventsViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/events/list1/')
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_all_event_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/events/list1/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/events/new', data={'item_text': 'Новое событие'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новое событие')

    def test_redirects_after_POST(self):
        response = self.client.post('/events/new', data={'item_text': 'Новое событие'})
        self.assertRedirects(response, '/events/list1/')
