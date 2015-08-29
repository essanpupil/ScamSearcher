from django.core.management.base import BaseCommand, CommandError

from website_analyzer.models import ExtendHomepage, StringParameter
from website_analyzer.analyzer_lib import string_analyst, ratio_analysist,\
                                          crawl_website
from website_management.models import Homepage

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Executing string analyst to homepage'

    def handle(self, *args, **options):
        homepages = Homepage.objects.exclude(
                extendhomepage__whitelist=True,
                extendhomepage__use_as_parameter=True)
        order_hp = homepages.order_by(
                            'extendhomepage__times_ratio_analyzed')
        if order_hp[0].extendhomepage.full_crawled == 0:
            crawl_website(order_hp[0])
        ratio_analysist(order_hp[0].id)
