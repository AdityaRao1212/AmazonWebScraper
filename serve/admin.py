from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Scraped, FastScraped
# Register your models here.

@admin.register(Scraped)
class ScrapedAdmin(ImportExportModelAdmin):
    list_display = ('brands', 'selling_price', 'rating', 'names')

admin.site.register(FastScraped)