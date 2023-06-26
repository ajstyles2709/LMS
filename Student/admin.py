from django.contrib import admin
from .models import Item, ReserveItem
# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['Id','Name','Category','AuthorName','YearOfPublished']


@admin.register(ReserveItem)
class ReserveItemAdmin(admin.ModelAdmin):
    list_display=['Id','ItemId','UserId','Category','DateOfIssue','DateOfReturn']