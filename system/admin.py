from django.contrib import admin
from system import models


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('StudentID','Name', 'sum')

admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Teacher)
