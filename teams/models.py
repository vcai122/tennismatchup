from django.db import models

class Default(models.Model):
    min_games = models.IntegerField()
    max_games = models.IntegerField()
    # TODO max players playing 6 games

class Match(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Game(models.Model):
    opponent_score = models.IntegerField(default=6)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    manually_assigned = models.BooleanField(default=False)

    def expected_win(self):
        return False
    expected_win.boolean = True

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

class SinglesGame(Game):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, null=True, blank=True)

    def expected_win(self):
        return self.player.s >= self.opponent_score
    expected_win.boolean = True

class DoublesGame(Game):
    player_one = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='player_one', null=True, blank=True)
    player_two = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='player_two', null=True, blank=True)

    def expected_win(self):
        return self.player_one.d + self.player_two.d >= self.opponent_score*2
    expected_win.boolean = True

class Player(models.Model):
    name = models.CharField(max_length=200)
    available_matches = models.ManyToManyField(Match)
    s = models.IntegerField(default=6)
    d = models.IntegerField(default=6)
    doubles_partners = models.ManyToManyField('self')
    max_single_games = models.IntegerField(default=10)
    min_double_games = models.IntegerField(default=2)

    def __str__(self):
        return self.name
        # return f'{self.name} ({self.s}, {self.d})'


    # TODO spread out