from django.core.management.base import BaseCommand
from teams.models import Match, Player, SinglesGame, DoublesGame
from django.db.models import F, Sum

class Command(BaseCommand):
    help = 'Prints in CSV format'

    def handle(self, *args, **options):
        # for match in Match.objects.all():
        #     print(match.name)
        #     s1, s2 = SinglesGame.objects.filter(match=match).order_by('id')
        #     print(f's1: {s1.player.name}')
        #     print(f's2: {s2.player.name}')
        #     d1, d2, d3 = DoublesGame.objects.filter(match=match).order_by('id')
        #     print(f'd1: {d1.player_one.name} {d1.player_two.name}')
        #     print(f'd2: {d2.player_one.name} {d2.player_two.name}')
        #     print(f'd3: {d3.player_one.name} {d3.player_two.name}')

        # for player in Player.objects.all():
        #     total_games = SinglesGame.objects.filter(player=player).count() + DoublesGame.objects.filter(player_one=player).count() + DoublesGame.objects.filter(player_two=player).count()
        #     print(f'{player.name}: {total_games}')
        num_singles = max(
            match.singlesgame_set.count()
            for match in Match.objects.all()
        )
        num_doubles = max(
            match.doublesgame_set.count()
            for match in Match.objects.all()
        )
        cols = ['Name'] + [f's{i+1}' for i in range(num_singles)] + [f'd{i+1}' for i in range(num_doubles)]

        print(','.join(cols))

        for match in Match.objects.all():
            row = [match.name]
            s_data = [
                # game.player.name
                str(game.player.s - game.opponent_score)
                for game in match.singlesgame_set.all().order_by('-player__s')
            ]
            d_data = [
                # f'{game.player_one.name} {game.player_two.name}'
                str((game.player_one.d + game.player_two.d) / 2 - game.opponent_score)
                for game in match.doublesgame_set.all() # TODO order by 
            ]

            row = (
                [match.name] 
                + s_data + [""] * (num_singles - len(s_data))
                + d_data + [""] * (num_doubles - len(d_data))
            )

            print(','.join(row))
            


        

        
