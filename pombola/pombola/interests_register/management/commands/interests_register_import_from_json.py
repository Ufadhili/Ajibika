import json
import sys
from datetime import date

from django.core.management.base import LabelCommand, CommandError

from pombola.core.models import Person
from ...models import Release, Category, Entry, EntryLineItem

class Command(LabelCommand):
    help = 'Import entries from our own JSON format'
    args = '<JSON file>'

    def handle_label(self,  input_filename, **options):

        with open(input_filename) as fp:
            data = json.load(fp)
            for grouping in data:
                self.handle_grouping(grouping)

    def handle_grouping(self, grouping):
        # print grouping

        person = Person.objects.get(**grouping['person'])

        release, _  = Release.objects.get_or_create(**grouping['release'])
        category, _ = Category.objects.get_or_create(**grouping['category'])

        # check that there are no entries for the given person, release and
        # category combination. This is because it is much easier to error if
        # there might be duplication that it is to detect and skip entries that
        # have already been created.
        entry_args = dict(person=person, release=release, category=category)
        if Entry.objects.filter(**entry_args).exists():
            raise Exception("Found existing entries for {person}, {category} and {release}. Please delete before continuing.".format(**entry_args))

        sort_order = 0
        for lines in grouping['entries']:
            sort_order += 1
            entry = Entry.objects.create(sort_order=sort_order, **entry_args)
            # print entry
            for key, value in lines.items():
                line_item = EntryLineItem.objects.create(entry=entry, key=key, value=value)
