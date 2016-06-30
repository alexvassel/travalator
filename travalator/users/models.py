# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Tourist(User):
    class Gender:
        choices = {True: _('male'), False: _('female')}

    class Martial:
        choices = {0: _('married')}

    gender = models.NullBooleanField(_('gender'), blank=True, null=True,
                                     choices=(Gender.choices.items()))
    age = models.PositiveSmallIntegerField(_('age'), blank=True, null=True)
    martial_status = models.PositiveSmallIntegerField(_('martial status'), null=True, blank=True,
                                                      choices=Martial.choices.items())

    @cached_property
    def social(self):
        return self.socialaccount_set.first()

    class Meta:
        verbose_name = 'Tourist'


class Company(User):
    inn = models.CharField(_('inn'), max_length=12, validators=[MinLengthValidator(10)])
    kpp = models.CharField(_('kpp'), blank=True, max_length=9, default='',
                           validators=[MinLengthValidator(9)])
    address = models.CharField(_('address'), max_length=255)
    phone = PhoneNumberField(_('phone'), max_length=12)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
