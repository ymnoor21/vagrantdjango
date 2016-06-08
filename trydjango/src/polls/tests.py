import datetime

from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.core.urlresolvers import reverse


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['top_5_questions'], [])

    def test_index_view_with_future_question(self):
        create_question('When are you coming?', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['top_5_questions'], [])

    def test_index_view_with_past_question(self):
        create_question('When did you come?', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['top_5_questions'],
            ['<Question: When did you come?>'])

    def test_index_view_with_past_and_future_question(self):
        create_question('Where were you?', days=-30)
        create_question('Where will you be?', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['top_5_questions'],
            ['<Question: Where were you?>']
        )

    def test_index_view_with_two_past_question(self):
        create_question('When did you come?', days=-30)
        create_question('Who else came with you?', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['top_5_questions'],
            ['<Question: Who else came with you?>',
             '<Question: When did you come?>'])


class QuestionDetailView(TestCase):
    def test_details_view_with_no_question(self):
        response = self.client.get(reverse('polls:details', args=[123]))
        self.assertEqual(response.status_code, 404)

    def test_details_with_past_question(self):
        choices = ['Yes', 'No']

        question = create_question('Were you there?', days=-30)
        question.choice_set.create(choice_text=choices[0], votes=1)
        question.choice_set.create(choice_text=choices[1], votes=0)
        question.save()

        response = self.client.get(reverse(
            'polls:details',
            args=[question.id]
        ))

        self.assertContains(response, question.question_text)
        for choice in question.choice_set.all():
            self.assertContains(response, choice)

    def test_details_with_future_question(self):
        choices = ['Yes', 'No']

        question = create_question('Were you there?', days=30)
        question.choice_set.create(choice_text=choices[0], votes=1)
        question.choice_set.create(choice_text=choices[1], votes=0)
        question.save()

        response = self.client.get(reverse(
            'polls:details',
            args=[question.id]
        ))

        self.assertEquals(response.status_code, 404)
