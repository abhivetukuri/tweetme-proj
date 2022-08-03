from django.contrib import admin

#Can add a bunch of functionality to the admin client of the website
#Built by Django and accessed with /admin on searchbar of site url


# Register your models here.
from .models import Tweet

class TweetAdmin(admin.ModelAdmin):
    #list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Tweet

admin.site.register(Tweet, TweetAdmin)
