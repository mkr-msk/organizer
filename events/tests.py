from django.test import TestCase
from events.models import Item, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'Первый элемент списка'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Второй элемент списка'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Первый элемент списка')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Второй элемент списка')
        self.assertEqual(second_saved_item.list, list_)


class EventsViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/events/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        response = self.client.get(f'/events/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'другой элемент 1 списка')
        self.assertNotContains(response, 'другой элемент 2 списка')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/events/new', data={'item_text': 'Новое событие'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новое событие')

    def test_redirects_after_POST(self):
        response = self.client.post('/events/new', data={'item_text': 'Новое событие'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/events/{new_list.id}/')


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        coorrect_list = List.objects.create()

        self.client.post(
            f'/events/{coorrect_list.id}/add_item',
            data={'item_text': 'Новый элемент существующего списка'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Новый элемент существующего списка')
        self.assertEqual(new_item.list, coorrect_list)

    def test_redirect_to_list_view(self):
        other_list = List.objects.create()
        coorrect_list = List.objects.create()

        response = self.client.post(
            f'/events/{coorrect_list.id}/add_item',
            data={'item_text': 'Новый элемент существующего списка'}
        )
        
        self.assertRedirects(response, f'/events/{coorrect_list.id}/')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        coorrect_list = List.objects.create()
        response = self.client.get(f'/events/{coorrect_list.id}/')
        self.assertEqual(response.context['list'], coorrect_list)
