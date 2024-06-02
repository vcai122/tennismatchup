from django.core.management.base import BaseCommand
from teams.models import Match, Player, SinglesGame, DoublesGame
from pulp import LpVariable, LpProblem, LpStatus, value, lpSum, LpMaximize, lpDot
import itertools

class Command(BaseCommand):
    help = 'Solve the schedule'

    def _get_skill_penalty(self, my_score, opp_score):
        diff = abs(my_score - opp_score)
        if diff <= 1:
            return 0
        scale = 8 if opp_score > my_score else 1
        return 2 ** diff * scale

    def handle(self, *args, **options):
        PENALTY = 1000000 # something much larger than other penalties
        min_play, max_play = 4, 6

        matches = Match.objects.all()
        single_games = SinglesGame.objects.all()
        double_games = DoublesGame.objects.all()
        players = Player.objects.all()

        model = LpProblem('Tennis', LpMaximize)

        singles = LpVariable.dicts('Single', (single_games, players), cat='Binary')
        doubles = LpVariable.dicts('Double', (double_games, players), cat='Binary')

        # a player can only be assigned to one game per match
        for match in matches:
            for player in players:
                model += lpSum(singles[game][player] for game in match.singlesgame_set.all()) + lpSum(doubles[game][player] for game in match.doublesgame_set.all()) <= 1

        # each game must have the correct number of players
        for game in single_games:
            model += lpSum(singles[game][player] for player in players) == 1
        for game in double_games:
            model += lpSum(doubles[game][player] for player in players) == 2

        # each game manually assigned must be played
        for game in single_games:
            if game.manually_assigned:
                model += singles[game][game.player] == 1
        for game in double_games:
            if game.manually_assigned:
                model += doubles[game][game.player_one] == 1
                model += doubles[game][game.player_two] == 1

        # each player must play between min_play and max_play games
        for player in players:
            total_games = lpSum(singles[game][player] for game in single_games) + lpSum(doubles[game][player] for game in double_games)
            model += total_games >= min_play
            model += total_games <= max_play
        
        # players can only go to games they are available for
        for player in players:
            for game in single_games:
                model += singles[game][player] <= player.available_matches.filter(id=game.match.id).exists()
            for game in double_games:
                model += doubles[game][player] <= player.available_matches.filter(id=game.match.id).exists()

        # makes sure double pairs are close in skill
        for game in double_games:
            for p1, p2 in itertools.combinations(players, 2):
                # (1, 1) -> 1, (1, 0) -> 0, (0, 1) -> 0, (0, 0) -> -1
                plus_or_minus = doubles[game][p1] + doubles[game][p2] - 1

                volunatary_partners = p1.doubles_partners.filter(id=p2.id).exists() or p2.doubles_partners.filter(id=p1.id).exists()
                if not volunatary_partners and abs(p1.d - p2.d) > 2:
                    model += plus_or_minus <= 0 # cannot play together

        # satisfy max_single_games and min_double_games
        for player in players:
            model += lpSum(singles[game][player] for game in single_games) <= player.max_single_games
            model += lpSum(doubles[game][player] for game in double_games) >= player.min_double_games

        # order among matches must make sense based on skill
        for match in matches:
            for query_set, curr_games, scores in [
                (single_games, singles, players.values_list('s', flat=True)), 
                (double_games, doubles, players.values_list('d', flat=True))
            ]:
                match_games = list(query_set.filter(match=match).order_by('-opponent_score'))
                prev_scores = [lpDot([curr_games[match_games[0]][player] for player in players], scores)]
                for i in range(1, len(match_games)):
                    curr_score = lpDot([curr_games[match_games[i]][player] for player in players], scores)
                    if match_games[i].opponent_score == match_games[i-1].opponent_score:
                        prev_scores.append(curr_score)
                    else:
                        for prev_score in prev_scores:
                            model += curr_score <= prev_score
                        prev_scores = [curr_score]




        double_penalties = LpVariable.dicts('DoublePenalty', double_games, lowBound=0, cat='Continuous')
        for game in double_games:
            for p1, p2 in itertools.combinations(players, 2):
                plus_or_minus = doubles[game][p1] + doubles[game][p2] - 1
                volunatary_partners = p1.doubles_partners.filter(id=p2.id).exists() or p2.doubles_partners.filter(id=p1.id).exists()
                penalty = PENALTY * (not volunatary_partners)
                model += double_penalties[game] >= plus_or_minus * penalty
        
        single_skill_gap_penalty = LpVariable.dicts('SingleSkillGapPenalty', single_games, lowBound=0, cat='Continuous')
        double_skill_gap_penalty = LpVariable.dicts('DoubleSkillGapPenalty', double_games, lowBound=0, cat='Continuous')
        for game in single_games:
            for player in players:
                penalty = self._get_skill_penalty(player.s, game.opponent_score)
                model += single_skill_gap_penalty[game] >= singles[game][player] * penalty
        for game in double_games:
            for p1, p2 in itertools.combinations(players, 2):
                # makes sure the total skill of the pair is close to the opponent
                plus_or_minus = doubles[game][p1] + doubles[game][p2] - 1
                penalty = self._get_skill_penalty((p1.d - p2.d)/2, game.opponent_score)
                model += double_skill_gap_penalty[game] >= plus_or_minus * penalty

        single_wins = LpVariable.dicts('SingleWin', single_games, upBound=0, cat='Continuous')
        double_wins = LpVariable.dicts('DoubleWin', double_games, upBound=0, cat='Continuous')
        for game in single_games:
            for player in players:
                player_wins = 0 if player.s >= game.opponent_score else -1
                model += single_wins[game] <= singles[game][player] * player_wins # enforce <= -1 if lose
        
        for game in double_games:
            for p1, p2 in itertools.combinations(players, 2):
                player_wins = 0 if p1.d + p2.d >= game.opponent_score*2 else -1
                plus_or_minus = doubles[game][p1] + doubles[game][p2] - 1
                # enforce <= -1 iff lose (player_wins=-1) and playing the game (plus_or_minus == 1)
                model += double_wins[game] <= plus_or_minus * player_wins 

        total_win = lpSum(single_wins) + lpSum(double_wins)
        skill_penalty = lpSum(single_skill_gap_penalty) + lpSum(double_skill_gap_penalty)
        double_mispair_penalty = lpSum(double_penalties)
        optimum = total_win - skill_penalty - double_mispair_penalty
        model += optimum


        res = model.solve()


        print(value(optimum))
        print(value(total_win), value(skill_penalty), value(double_mispair_penalty))







        if (status := LpStatus[res]) != 'Optimal':
            self.stdout.write(self.style.ERROR(f'No solution could be found. Status: {status}'))
            return
    
        for game in single_games:
            game.player, = [player for player in players if value(singles[game][player]) == 1]
            game.save()

        for game in double_games:
            game.player_one, game.player_two = [player for player in players if value(doubles[game][player]) == 1]
            game.save()

        total_expected_wins = sum(s.expected_win() for s in SinglesGame.objects.all()) + sum(d.expected_win() for d in DoublesGame.objects.all())
        print(f'Total expected wins: {total_expected_wins} out of {SinglesGame.objects.count() + DoublesGame.objects.count()} games')
            
        
