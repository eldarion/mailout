import datetime

from django.core.mail import send_mass_mail
from django.conf import settings
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.template import RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from mailout.email_lists import email_lists
from mailout.forms import CampaignCreateForm
from mailout.models import Campaign, CampaignLog, EmailTemplate


@staff_member_required
def dashboard(request):
    ctx = {
        "email_lists": email_lists.keys(),
    }
    return render(request, "mailout/dashboard.html", ctx)


@staff_member_required
def campaign_create(request):
    if request.method == "POST":
        form = CampaignCreateForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            return redirect("campaign_review", campaign.pk)
    else:
        initial = {"from_address": settings.CONTACT_EMAIL}
        if "email_list" in request.GET:
            initial["email_list"] = request.GET["email_list"]
        form = CampaignCreateForm(initial=initial)
    ctx = {
        "form": form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("mailout/campaign_create.html", ctx)


@staff_member_required
def campaign_review(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    ctx = {
        "campaign": campaign,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("mailout/campaign_review.html", ctx)


@staff_member_required
def campaign_submit(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    campaigns = Campaign.objects.select_related("email_template")
    campaign = get_object_or_404(campaigns, pk=pk)
    messages = []
    for email, email_ctx in campaign:
        messages.append((
            campaign.email_template.render_subject(email_ctx),
            campaign.email_template.render_body(email_ctx),
            campaign.from_address,
            [email],
        ))
        CampaignLog.objects.create(campaign=campaign, email=email)
    send_mass_mail(messages)
    campaign.sent = datetime.datetime.now()
    campaign.save()
    return redirect("campaign_review", campaign.pk)


@staff_member_required
def campaign_email_preview(request, pk, email):
    campaigns = Campaign.objects.select_related("email_template")
    campaign = get_object_or_404(campaigns, pk=pk)
    email_ctx = {}
    try:
        email_ctx = dict(campaign)[email]
    except KeyError:
        raise Http404("Email not found in campaign")
    ctx = {
        "campaign": campaign,
        "subject": campaign.email_template.render_subject(email_ctx),
        "email": email,
        "from_address": campaign.from_address,
        "body": campaign.email_template.render_body(email_ctx),
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("mailout/_campaign_email_preview.html", ctx)


@staff_member_required
def email_list_detail(request, label):
    try:
        email_list_func = email_lists[label]["list"]
    except KeyError:
        raise Http404
    ctx = {
        "email_list_name": label,
        "email_list": list(email_list_func()),
        "campaigns": Campaign.objects.filter(email_list=label),
    }
    return render(request, "mailout/email_list_detail.html", ctx)


@staff_member_required
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    ctx = {
        "campaign": campaign,
    }
    return render(request, "mailout/campaign_detail.html", ctx)
