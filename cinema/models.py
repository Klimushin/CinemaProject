from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

from user.models import Customer


class Hall(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Hall name'))
    slug = models.SlugField(max_length=128, unique=True)
    size = models.PositiveSmallIntegerField(verbose_name=_('Hall size'))

    class Meta:
        verbose_name = _('Hall')
        verbose_name_plural = _('Halls')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save method"""

        if not self.slug:
            self.slug = slugify(self.name)

        super(Hall, self).save(*args, **kwargs)


class Session(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Hall'))
    start_time = models.TimeField(verbose_name=_('Start time'))
    end_time = models.TimeField(verbose_name=_('End time'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(verbose_name=_('End date'))
    price = models.PositiveSmallIntegerField(verbose_name=_('Ticket price'))
    status = models.BooleanField(default=True, verbose_name=_('Status'), blank=True)

    class Meta:
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')

    @property
    def get_show_date(self):
        return f'{self.start_date.day}.{self.start_date.month}.{self.start_date.year}' \
               f' - ' \
               f'{self.end_date.day}.{self.end_date.month}.{self.end_date.year}'

    def check_status(self):
        if self.end_date < timezone.now().date():
            self.status = False
        return self.status

    def __str__(self):
        return f'Session {self.id}'

    def save(self, *args, **kwargs):
        self.check_status()
        super().save(*args, **kwargs)


class Ticket(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='purchased_tickets',
        verbose_name=_('Purchase'), blank=True
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name='session_tickets',
        verbose_name=_('Session'),
        blank=True
    )
    quantity = models.PositiveSmallIntegerField(verbose_name=_('Quantity ticket'))

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return f'Ticket {self.id}'
