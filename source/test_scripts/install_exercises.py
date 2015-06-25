import django, logging, logging.config, os, sys

os.environ["DJANGO_SETTINGS_MODULE"] = "django_site.settings"
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir , "../"))
django.setup()

from cpe.models import *

assert(Exercise.objects.all().count() == 0)

Exercise.objects.create(id = 1  , name = 'segment_tree.get_size()'    , cf_contest_id = 100535, cf_problem_index = "A")
Exercise.objects.create(id = 2  , name = 'segment_tree.init()'        , cf_contest_id = 100535, cf_problem_index = "B")

print("Everything is fine")
print("{cnt} exercises created".format(cnt = Exercise.objects.all().count()))