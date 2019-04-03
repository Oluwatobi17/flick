from django.contrib import admin
from .models import User, Following, Contact, Quoteoftheday, Jokeoftheday, Motivationoftheday,Selectionoftheday,Oneofakind

# Register your models here.

admin.site.register(User)
admin.site.register(Following)
admin.site.register(Contact)
admin.site.register(Quoteoftheday)
admin.site.register(Jokeoftheday)
admin.site.register(Motivationoftheday)
admin.site.register(Selectionoftheday)
admin.site.register(Oneofakind)