import sys,os
from audit.backend import user_interactive
if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
    import django
    django.setup()#手动注册django所有的App
    obj=user_interactive.UserShell(sys.argv)
    obj.start()

