"helper module for website_management app."
from django.db import IntegrityError, transaction
import tldextract

from website_management.models import Webpage, Website, Domain


def add_url_to_webpage(url):
    """add url and its component to database"""
    ext = tldextract.extract(url)
    domain, _ = Domain.objects.get_or_create(name=ext.registered_domain)
    homepage, _ = Website.objects.get_or_create(name='.'.join(ext),
                                                domain=domain)
    try:
        with transaction.atomic():
            Webpage.objects.create(url=url, homepage=homepage)
    except IntegrityError:
        raise IntegrityError


def add_list_url_to_webpage(urls):
    """add list url and their components to database"""
    for url in urls:
        try:
            add_url_to_webpage(url)
        except IntegrityError:
            continue
