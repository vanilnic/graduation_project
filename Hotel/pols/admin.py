from django.contrib import admin
from .models import User, Hotel, Favorites, Rooms, Booking, Reviews

# Register your models here.
admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Favorites)
admin.site.register(Rooms)
admin.site.register(Booking)
admin.site.register(Reviews)