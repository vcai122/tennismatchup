from django.core.management.base import BaseCommand
from teams.models import Match, Player, SinglesGame, DoublesGame

class Command(BaseCommand):
    help = 'Create matches and players'

    def handle(self, *args, **options):
        NUM_SINGLES, NUM_DOUBLES = 2, 3

        Match.objects.all().delete()
        Player.objects.all().delete()
        SinglesGame.objects.all().delete()
        DoublesGame.objects.all().delete()
        
        matches = [
            Match(name=f'Match {i}', description=f'')
            for i in range(10)
        ]
        Match.objects.bulk_create(matches)
        SinglesGame.objects.bulk_create([
            SinglesGame(match=match)
            for match in matches
            for _ in range(NUM_SINGLES)
        ])

        DoublesGame.objects.bulk_create([
            DoublesGame(match=match)
            for match in matches
            for _ in range(NUM_DOUBLES)
        ])
            
        
        players = [
            Player(name=f'Player {i}')
            for i in range(17)
        ]
        Player.objects.bulk_create(players)
        for player in players:
            player.available_matches.set(matches)
            player.doubles_partners.set(players)
            player.save()

        
