from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Script, MarketChart



class MarketUserAdmin(UserAdmin):
    search_fields = ['username']
    list_display = ('id', 'username')

    fieldsets = UserAdmin.fieldsets + (
        ('User Info', {'fields': (
            'contact_number',
            'balance',
            'user_type'
        )}),
    )


class ScriptAdmin(admin.ModelAdmin):
    list_display = ['name']


class MarketAdmin(admin.ModelAdmin):
    list_display = ['script', 'date', 'brand', 'sales_rank', 'share', 'share_perc']

class MarketChartAdmin(admin.ModelAdmin):
    list_display = ['id', 'script', 'chart_img']



admin.site.register(User, MarketUserAdmin)
admin.site.register(Script, ScriptAdmin)
admin.site.register(MarketChart, MarketChartAdmin)