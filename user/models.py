from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext as _


class Customer(AbstractUser):
    balance = models.PositiveIntegerField(
        verbose_name=_('Amount'),
        default=0,
        blank=False
    )
