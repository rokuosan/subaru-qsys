from django.contrib import admin

from .models.contest import Contest
from .models.history import History
from .models.player import Player
from .models.question import Category, Difficulty, Question
from .models.team import Team

# Register your models here.
admin.site.register(Player)
admin.site.register(Contest)
admin.site.register(History)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Difficulty)
admin.site.register(Team)
