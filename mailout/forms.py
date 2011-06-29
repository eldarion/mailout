from django import forms

from mailout.models import Campaign


class CampaignCreateForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ["created", "sent"]
