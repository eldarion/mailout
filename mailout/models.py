import datetime

from django.db import models
from django.template import Template, Context

from mailout.email_lists import email_lists


class EmailTemplate(models.Model):
    
    label = models.CharField(max_length=100)
    subject = models.TextField()
    body = models.TextField()
    
    def __unicode__(self):
        return self.label
    
    def render_subject(self, ctx=None):
        return self.render(self.subject, ctx)
    
    def render_body(self, ctx=None):
        return self.render(self.body, ctx)
    
    def render(self, content, ctx=None):
        """
        Render the template data through the Django templating engine.
        """
        if ctx is None:
            ctx = {}
        t = Template(content)
        return t.render(Context(ctx))


class Campaign(models.Model):
    
    from_address = models.CharField(max_length=150)
    email_template = models.ForeignKey(EmailTemplate)
    email_list = models.CharField(max_length=50, choices=email_lists.choices())
    created = models.DateTimeField(default=datetime.datetime.now)
    sent = models.DateTimeField(null=True)
    
    def __iter__(self):
        return iter(email_lists[self.email_list]["list"]())
    
    def results(self):
        result_func = email_lists[self.email_list]["results"]
        if result_func is None:
            raise NotImplementedError("no results function found for '%s'" % self.email_list)
        return iter(result_func())
    
    def result_counts(self):
        if not hasattr(self, "_result_counts"):
            counts = len([x for x in self.results() if x[1]]), len(list(self.results()))
            self._result_counts = counts
        else:
            counts = self._result_counts
        return counts


class CampaignLog(models.Model):
    
    campaign = models.ForeignKey(Campaign)
    email = models.EmailField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)
