from random import choice
from string import ascii_lowercase

from django.db import models

from comment import settings


class CommentQuerySet(models.QuerySet):
    def filter_accepted(self):
        return self.filter(status='a')

    def filter_parents(self):
        return self.filter(parent__isnull=True)

    def order_newest(self):
        return self.order_by('-posted')

    def order_oldest(self):
        return self.order_by('posted')

    @staticmethod
    def generate_urlhash():
        return ''.join(choice(ascii_lowercase) for _ in range(settings.COMMENT_URLHASH_LENGTH))


class ReactionQuerySet(models.QuerySet):
    def get_reacts(self):
        from comment.models import React

        reacts = React.objects.all()
        return {react: self.filter(react=react) for react in reacts}

    def get_users(self):
        return [reaction.user for reaction in self.all()]
