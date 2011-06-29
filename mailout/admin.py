from django.contrib import admin

from mailout.models import EmailTemplate, Campaign, CampaignLog


admin.site.register(EmailTemplate)
admin.site.register(Campaign)
admin.site.register(CampaignLog,
    list_display = ["pk", "campaign", "email", "timestamp"],
    list_filter = ["campaign"]
)