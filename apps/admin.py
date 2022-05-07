from django_better_admin_arrayfield.models.fields import ArrayField
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.contrib import admin

from .models import Task, Solution


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin, DynamicArrayMixin):
    shown_fields = ["name", "text", "task", "code", "call", "data", "default", "expected", "is_pub"]
    list_display = ["id"] + shown_fields
    list_editable = shown_fields
    list_filter = shown_fields


@admin.register(Solution)
class TaskAdmin(admin.ModelAdmin):
    shown_fields = ["id", "user", "task", "resolve"]
    list_display = shown_fields
    list_filter = shown_fields
