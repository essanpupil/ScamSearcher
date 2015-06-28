import tldextract

from django.utils import timezone
from django.db import IntegrityError, transaction

from website_management.models import Homepage, Webpage, Domain
from .models import ExtendHomepage, StringParameter, StringAnalysist
from .models import ExtendWebpage, ExtendDomain

from webscraper.pagescraper import PageScraper

def string_analyst(hp_id):
    """function to do string analyst to homepage"""
    hp = Homepage.objects.get(id=hp_id)
    exthp, created = ExtendHomepage.objects.get_or_create(homepage=hp)
    params = StringParameter.objects.all()
    for web in hp.webpage_set.all():
        for param in params:
            if param.sentence in web.extendwebpage.text_body:
                StringAnalysist.objects.create(webpage=web,
                                               parameter=param,
                                               find=True)
                if param.definitive:
                    exthp.scam = True
                    exthp.save()
            else:
                StringAnalysist.objects.create(webpage=web,
                                               parameter=param,
                                               find=False)


def add_url_to_webpage(url):
    """add url and its component to database"""
    ext = tldextract.extract(url)
    try:
        with transaction.atomic():
            dom, crtd = Domain.objects.get_or_create(name=ext.registered_domain)
            ExtendDomain.objects.create(domain=dom)
    except:
        pass
    try:
        with transaction.atomic():
            hp, crtd2 = Homepage.objects.get_or_create(name='.'.join(ext),
                                                       domain=dom)
            ExtendHomepage.objects.create(homepage=hp)
    except:
        pass
    try:
        with transaction.atomic():
            web = Webpage.objects.create(url=url, homepage=hp)
            ExtendWebpage.objects.create(webpage=web)
    except IntegrityError:
        raise IntegrityError


def add_scam_url_website(url):
    """add url and its component to database"""
    ext = tldextract.extract(url)
    dom, crtd = Domain.objects.get_or_create(name=ext.registered_domain)
    ExtendDomain.objects.create(domain=dom)
    hp, crtd2 = Homepage.objects.get_or_create(name='.'.join(ext),
                                               domain=dom)
    ExtendHomepage.objects.create(homepage=hp)
    try:
        with transaction.atomic():
            web = Webpage.objects.create(url=url, homepage=hp)
            ExtendWebpage.objects.create(webpage=web)
            exthp = ExtendHomepage.objects.get(homepage=hp)
            exthp.scam = True
            exthp.save()
    except IntegrityError:
        raise IntegrityError


def add_list_url_to_webpage(urls):
    """add list url and their components to database"""
    for url in urls:
        try:
            add_url_to_webpage(url)
        except IntegrityError:
            continue

def fill_text_body(extw):
    "Function to fill text_body of an ExtendWebpage object"
    page = PageScraper()
    text = page.get_text_body(html=extw.webpage.html_page)
    extw.text_body = text
    extw.save()


def string_analysist(homepage):
    """function to doing string analysist on to website/homepage model object.
    required website_management.models.Homepage as argument"""
    hari_ini = timezone.now()
    parameters = StringParameter.objects.all()
    webpages = homepage.webpage_set.all()
    for parameter in parameters:
        for webpage in webpages:
            newest_string_analysist = StringAnalysist.objects.filter(
                    webpage=webpage,
                    parameter=parameter).order_by('time').reverse()
            if newest_string_analysist.count() == 0:
                extw, created = ExtendWebpage.objects.get_or_create(
                        webpage=webpage)
                if parameter.sentence in extw.text_body:
                    StringAnalysist.objects.create(webpage=webpage,
                            parameter=parameter,
                            find=True)
                else:
                    StringAnalysist.objects.create(webpage=webpage,
                            parameter=parameter,
                            find=False)
            else:
                if (hari_ini - newest_string_analysist[0].time).days == 0:
                    continue
                else:
                    extw, created = ExtendWebpage.objects.get_or_create(
                            webpage=webpage)
                    if parameter.sentence in extw.text_body:
                        StringAnalysist.objects.create(webpage=webpage,
                                parameter=parameter,
                                find=True)
                    else:
                        StringAnalysist.objects.create(webpage=webpage,
                                parameter=parameter,
                                find=False)
            continue
        continue


def crawl_website(homepage):
    """function to fetch html code and url of a website, start from available
    webpages in the database. The only accepted argument in Homepage object."""
    keep_crawling = True
    while True:
        for webpage in homepage.webpage_set.all():
            page = PageScraper()
            page.fetch_webpage(webpage.url)
            webpage.html_page = page.html
            extw, created = ExtendWebpage.objects.get_or_create(
                    webpage=webpage)
            extw.text_body = page.get_text_body()
            extw.save()
            webpage.save()
            add_list_url_to_webpage(page.ideal_urls())
        if not homepage.webpage_set.filter(html_page__isnull=True).exists():
            break


