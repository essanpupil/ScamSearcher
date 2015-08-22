from django.core.management.base import BaseCommand, CommandError

from website_management.models import Query, Search, Webpage
from search_extractor.google_search import GoogleSearch
from website_management.management_lib import add_list_url_to_webpage


class Command(BaseCommand):
    args = 'Arguments are not needed'
    help = "Search webpages with saved queries"
    
    def handle(self, *args, **options):
        query = Query.objects.all().order_by('times_used')
        if query:
            search = GoogleSearch(query[0].keywords)
            search.start_search()
            add_list_url_to_webpage(search.search_result)
            for url in search.search_result:
                webpage = Webpage.objects.get(url=url)
                saved_search = Search.objects.create(webpage=webpage,
                                                     query=query[0]) 
            query[0].times_used += 1
            query[0].save(update_fields=['times_used'])
        else:
            print "Query database empty"
