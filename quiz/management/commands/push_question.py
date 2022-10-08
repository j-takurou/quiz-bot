from django.core.management.base import BaseCommand, CommandError
from quiz.views import push_question

class Command(BaseCommand):
    help = 'Push the question.'

    def add_arguments(self, parser):
        parser.add_argument('question_number', nargs=1, type=int)

    def handle(self, *args, **options):
        
        question_number = options['question_number'][0]
        print(question_number)
        push_question(question_number)
        self.stdout.write(f'Successfully pushed question {question_number}.')