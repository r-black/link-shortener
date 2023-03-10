from urllib.parse import urlparse

from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator, RegexValidator


class Link(models.Model):
    url = models.URLField(max_length=2048)
    alias = models.CharField(max_length=6, unique=True, validators=[
        MinLengthValidator(6),
        RegexValidator(
            regex=r'^[a-z0-9-_]+$',
            code='invalid_alias',
            message='Alias can only contain lowercase alphabets, numerals, underscores and hyphens',
        ),
    ])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alias} -> {self.url}"

    class Meta:
        ordering = ('-date_created', )

    def get_long_url_truncated(self, max_length=30, remove_schema=True):
        truncated_url = self.url
        if remove_schema:
            parsed_url = urlparse(truncated_url)
            scheme = parsed_url.scheme
            truncated_url = truncated_url[len(scheme) + 3:]
            if parsed_url.path == '/' and not parsed_url.fragment and not parsed_url.query:
                truncated_url = truncated_url[:-1]
        if len(truncated_url) > max_length:
            truncated_url = truncated_url[:max_length] + '...'
        return truncated_url

    def get_date_created(self):
        return str(self.date_created)

    def get_date_created_human_friendly(self):
        return self.date_created.strftime('%Y %b %d, %I:%M %p')

    def get_alias_path(self):
        return reverse('app_urls:alias', args=(self.alias,))

    def get_preview_path(self):
        return reverse('app_urls:preview', args=(self.alias,))

    def get_clicks(self):
        clicks = Click.objects.filter(link=self)
        clicks = clicks.aggregate(total_clicks=models.Sum('clicks_count'),)
        if clicks['total_clicks'] is None:
            clicks['total_clicks'] = 0
        return clicks


class Click(models.Model):
    link = models.ForeignKey(to=Link, on_delete=models.CASCADE)
    clicked_date = models.DateField(auto_now_add=True)
    clicks_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.link.alias}: {self.clicks_count}"
