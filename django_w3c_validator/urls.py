from django.views.generic.base import RedirectView, TemplateView
from django.conf.urls import patterns, url
from django.conf import settings


collapse = getattr(settings, 'VALIDATOR_COLLAPSE', True)
urlpatterns = patterns('',
    (r'^/?$', TemplateView.as_view(template_name='validation-base.html'), {'collapse': collapse}, 'validation'),
    (r'^/urls/?$', TemplateView.as_view(template_name='crawled-urls.txt', content_type='text/plain'), {}, 'crawled_urls'),
)