from django.contrib import admin

# Register your models here.
from .models import Match
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'opponent', 'tournament', 'score_display', 'result', 'venue', 'manager')
    list_filter = ('result', 'tournament', 'manager')
    search_fields = ('opponent', 'tournament', 'manager', 'scorers')
    date_hierarchy = 'date'
    def score_display(self, obj):
        return f"{obj.japan_score} - {obj.opponent_score}"
    score_display.short_description = "スコア"