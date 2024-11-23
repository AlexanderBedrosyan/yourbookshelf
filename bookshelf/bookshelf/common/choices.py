from django.db import models


class LevelChoices(models.TextChoices):
    AMATEUR = 'Amateur', 'Amateur'
    SEMI_PRO = 'Semi-Pro', 'Semi-Pro'
    PRO = 'Pro', 'Pro'
    WORLD_CLASS = 'World-Class', 'World-Class'
    KING = 'King of the book knowledges', 'King of the book knowledges'