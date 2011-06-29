from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r"^$", "mailout.views.dashboard", name="user_mailer_dashboard"),
    url(r"^campaign/create/$", "mailout.views.campaign_create", name="campaign_create"),
    url(r"^campaign/(\d+)/review/$", "mailout.views.campaign_review", name="campaign_review"),
    url(r"^campaign/(\d+)/email_preview/(.+)/$", "mailout.views.campaign_email_preview", name="campaign_email_preview"),
    url(r"^campaign/(\d+)/submit/$", "mailout.views.campaign_submit", name="campaign_submit"),
    url(r"^email_list/(\w+)/", "mailout.views.email_list_detail", name="email_list_detail"),
    url(r"^campaign/(\d+)/", "mailout.views.campaign_detail", name="campaign_detail"),
)
