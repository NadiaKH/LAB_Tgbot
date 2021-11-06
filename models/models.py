from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='User ID',
        unique=True
    )
    name = models.TextField(
        verbose_name='User Name'
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Profile'


class Message(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Text',
    )

    group_name = models.CharField(
        max_length=50,
        default='default_group',
    )

    created_at = models.DateTimeField(
        verbose_name='Receiving time',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Message{self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Message'


class Group(models.Model):

    group_name = models.CharField(
        max_length=50,
        verbose_name='Group',
        default='default_group',
    )

    profile = models.ForeignKey(
        to=Profile,
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f'Group{self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'Group'
        unique_together = (('profile', 'group_name'),)
