from django.contrib import admin
from .models import ToDo


# Register your models here. display todo
@admin.register(ToDo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "description", "date", "is_completed")
