from django.contrib import admin
from .models import User,Product

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)


admin.site.register(Product)