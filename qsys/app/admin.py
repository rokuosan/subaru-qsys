from django.contrib import admin

from .models.app_user import AppUser
from .models.category import CtfQuestionCategory
from .models.ctf_information import CtfInformation
from .models.difficulty import CtfQuestionDifficulty
from .models.history import CtfAnswerHistory
from .models.question import CtfQuestion
from .models.score import CtfScore
from .models.team import CtfTeam

# Register your models here.
admin.site.register(AppUser)
admin.site.register(CtfScore)
admin.site.register(CtfInformation)
admin.site.register(CtfQuestionCategory)
admin.site.register(CtfQuestionDifficulty)
admin.site.register(CtfAnswerHistory)
admin.site.register(CtfQuestion)
admin.site.register(CtfTeam)
