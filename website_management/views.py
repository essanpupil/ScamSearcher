"""views module to manage website data."""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from website_management.models import Website
from website_analyzer.models import SearchKeywords


def website_dashboard(request):
    """display info summary about saved webpages, homepage, & domain"""
    homepages = Website.objects.all()
    context = {'homepage_count': homepages.count(),
               'newest_5_homepage': []}
    for homepage in homepages.order_by('id').reverse()[0:5]:
        context['newest_5_homepage'].append(
            {'name': homepage.name, 'id': homepage.id})
    return render(request, 'website_management/dashboard.html', context)


def homepage_detail(request, hp_id):
    "display detail info of selected homepage"
    homepage = get_object_or_404(Website, id=hp_id)
    context = {
        'hpname': homepage.name,
        'hpid': homepage.id,
        'hpadded': homepage.date_added,
        'hpdomain': homepage.domain.name,
        'iddom': homepage.domain.id,
        'hpweb': []
    }
    for item in homepage.webpage_set.all():
        context['hpweb'].append({'url': item.url, 'id': item.id})
    return render(request, 'website_management/homepage_detail.html', context)


def view_all_homepages(request):
    """display all webpage"""
    homes = Website.objects.all().order_by('id').reverse()
    context = {'homes': []}
    for item in homes:
        context['homes'].append({
            'name': item.name,
            'date_added': item.date_added,
            'domain': item.domain,
            'id': item.id})
    paginator = Paginator(context['homes'], 10)
    page = request.GET.get('page')
    try:
        context['homes'] = paginator.page(page)
    except PageNotAnInteger:
        context['homes'] = paginator.page(1)
    except EmptyPage:
        context['homes'] = paginator.page(paginator.num_pages)
    return render(request,
                  'website_management/view_all_homepages.html', context)


def view_all_keywords(request):
    """display all keywords"""
    queries = SearchKeywords.objects.all().order_by('id').reverse()
    context = {'queries': []}
    for item in queries:
        context['queries'].append({'keyword': item.keywords,
                                   'date_added': item.date_added,
                                   'times_used': item.times_used,
                                   'id': item.id})
    return render(request,
                  'website_management/view_all_keywords.html', context)
