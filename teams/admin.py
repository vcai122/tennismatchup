from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

def box(content, width=70):
    return f'<span style="width: {width}px; display: inline-block;">{content}</span>'

def span(content):
    return f'<span>{content}</span>'

class SinglesGameInline(admin.StackedInline):  # or TabularInline
    model = SinglesGame
    can_delete = False
    extra = 0
    fields = ['opponent_score', 'player', 'match', 'manually_assigned']
    # readonly_fields = ['expected_win', 'skill_diff']

    def skill_diff(self, obj):
        return obj.player.s - obj.opponent_score
    

class DoublesGameInline(admin.StackedInline):  # or TabularInline
    model = DoublesGame
    can_delete = False
    extra = 0
    fields = ['opponent_score', 'player_one', 'player_two', 'match', 'manually_assigned']
    # readonly_fields = ['player_one', 'player_two', 'expected_win', 'skill_diff']

    def skill_diff(self, obj):
        return (obj.player_one.d + obj.player_two.d)/2 - obj.opponent_score

class SinglesGameInlinePlayer(SinglesGameInline):
    readonly_fields = ['opponent_score', 'match']
    fields = readonly_fields
    max_num=0

class DoubleGameInline1(DoublesGameInline): 
    fk_name = 'player_one'
    readonly_fields = ['opponent_score', 'match', 'player_two']
    fields = readonly_fields
    max_num=0

class DoubleGameInline2(DoublesGameInline):
    fk_name = 'player_two'
    readonly_fields = ['opponent_score', 'match', 'player_one']
    fields = readonly_fields
    max_num=0

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    inlines = [SinglesGameInline, DoublesGameInline]
    list_display = ('name', 'description', 'singles_games', 'doubles_games')

    def singles_games(self, obj):
        # wrap
        return mark_safe(span(
            ''.join(
                span(f's{i+1}: {box(game.player)}')
                for i, game in enumerate(obj.singlesgame_set.all())
            )
        ))
    
    def doubles_games(self, obj):
        return mark_safe(span(
            ''.join(
                span(f'd{i+1}: {box(game.player_one)} {box(game.player_two)}') 
                for i, game in enumerate(obj.doublesgame_set.all())
            )
        ))

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    inlines = [SinglesGameInlinePlayer, DoubleGameInline1, DoubleGameInline2]
    list_display = ('name', 's', 'd', 'max_single_games', 'min_double_games', 'partners', 'availability')

    def partners(self, obj):
        return ', '.join(p.name for p in obj.doubles_partners.all())
    
    def availability(self, obj):
        return ' '.join('v' if obj.available_matches.filter(id=match.id).exists() else 'x' for match in Match.objects.all().order_by('id'))

admin.register(Default)

