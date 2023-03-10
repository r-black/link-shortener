from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.timezone import datetime, timedelta
from django.views import View
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView

from .misc import (hash_encode,
                   get_absolute_short_url,
                   process_new_click)
from .forms import URLShortenerForm
from .models import Click, Link


class NewLinkView(FormView):
    template_name = 'app_urls/index.html'
    form_class = URLShortenerForm

    def form_valid(self, form):
        request = self.request
        original_alias = form.cleaned_data['alias']
        alias = original_alias.lower()
        url = form.cleaned_data['url']
        new_link = Link(url=url)
        try:
            latest_link = Link.objects.latest('id')
            if Link.objects.filter(alias__exact=alias).exists():
                # handle alias conflict
                new_link.alias = alias + '-' + hash_encode(latest_link.id + 1)
                messages.add_message(request, messages.INFO,
                                     'Short URL {} already exists so a new short URL was created.'
                                     .format(get_absolute_short_url(request, original_alias)))
                original_alias = new_link.alias
            else:
                new_link.alias = alias or hash_encode(latest_link.id + 1)
        except Link.DoesNotExist:
            new_link.alias = alias or hash_encode(1)
        new_link.save()
        return HttpResponseRedirect(reverse('app_urls:preview', args=(original_alias or new_link.alias,)))


class LinkPreview(DetailView):
    model = Link
    template_name = 'app_urls/preview.html'
    slug_url_kwarg = 'alias'
    slug_field = 'alias__iexact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context.update({
            'alias': obj.alias,
            'absolute_short_url': get_absolute_short_url(self.request, obj.alias, remove_schema=False),
            'url': obj.url,
        })
        return context


class LinkUpdateView(UpdateView):
    model = Link
    fields = ['url']
    slug_url_kwarg = 'alias'
    slug_field = 'alias__iexact'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('app_urls:analytics')


class DeleteLinkView(DeleteView):
    model = Link
    slug_url_kwarg = 'alias'
    slug_field = 'alias__iexact'
    success_url = reverse_lazy('app_urls:analytics')


class LinkRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        alias = kwargs.get('alias', '')
        extra = kwargs.get('extra', '')
        link = get_object_or_404(Link, alias__iexact=alias)
        process_new_click(link)
        return link.url + extra


class AnalyticsView(ListView):
    model = Link
    paginate_by = 10
    context_object_name = 'links'
    template_name = 'app_urls/analytics.html'


class ChartDataView(View):
    def get(self, request, *args, **kwargs):
        alias = kwargs.get('alias', '')
        link = get_object_or_404(Link, alias__iexact=alias)
        today = datetime.today()
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        if not start_date:
            start_date = today - timedelta(days=7)
        if not end_date:
            end_date = today
        clicks = Click.objects.filter(link=link, clicked_date__range=[start_date, end_date])
        chart_data = {}
        for click in clicks.iterator():
            str_date = str(click.clicked_date)
            if str_date in chart_data:
                chart_data[str_date] += click.clicks_count
            else:
                chart_data[str_date] = click.clicks_count
        return JsonResponse(data={
            'labels': list(chart_data.keys()),
            'data': list(chart_data.values())
        })
