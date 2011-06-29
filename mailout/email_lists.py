from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


class EmailListDict(object):
    
    def _load(self):
        if hasattr(self, "_lists"):
            return
        if not hasattr(settings, "MAILOUT_MODULES"):
            raise ImproperlyConfigured("You must define 'MAILOUT_MODULES' in settings")
        self._lists = {}
        for mp in settings.MAILOUT_MODULES:
            i = mp.rfind(".")
            path, module = path[:i], path[i+1:]
            m = import_module(mp)
            self._lists[module] = {
                "list": m.email_list,
                "results": getattr(m, "email_list_results", None),
            }
    
    def __getitem__(self, key):
        self._load()
        return self._lists[key]
    
    def keys(self):
        self._load()
        return self._lists.keys()


email_lists = EmailListDict()
