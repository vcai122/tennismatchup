from django.core.management.base import BaseCommand
from teams.models import Match, Player, DoublesGame

class Command(BaseCommand):
    help = 'Prints in CSV format'

    def handle(self, *args, **options):
        all_double_valid = True
        for game in DoublesGame.objects.all():
            if not(
                game.player_one.doubles_partners.filter(id=game.player_two.id).exists()
                or game.player_two.doubles_partners.filter(id=game.player_one.id).exists()
            ):
                all_double_valid = False
                print(f"{game.match.name}: {game.player_one.name} {game.player_two.name} are not partners")
        if all_double_valid: 
            print("All doubles games are valid")


        
    

        

        
