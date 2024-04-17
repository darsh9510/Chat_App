from django.contrib import admin

from .models import Massage,topic,Rooms,modarator,Anonumous

admin.site.register(Massage)
admin.site.register(topic)
admin.site.register(Rooms)
admin.site.register(modarator)
admin.site.register(Anonumous)