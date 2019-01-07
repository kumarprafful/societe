from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from account.models import User

from datetime import datetime

# Create your models here.
class Society(models.Model):
    class Meta:
        verbose_name= 'Society'
        verbose_name_plural = 'Societies'
    user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    society_name = models.CharField(max_length=1024, unique=True)
    slug = models.SlugField(_('slug'), db_index=True, max_length=2024, unique=True)
    president = models.CharField(max_length=1024)
    address = models.CharField(max_length=1024)
    date_of_creation = models.DateTimeField(default=datetime.now)

    def get_absolute_url(self):
        return reverse('record:society-dash', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.society_name)
        super(Society, self).save(*args, **kwargs)

    def __str__(self):
        return self.society_name

class SocietySetting(models.Model):
    society = models.OneToOneField(Society, on_delete=models.CASCADE)
    basic_share = models.IntegerField(default=200)
    interest_rate = models.DecimalField(default=0.01, max_digits=2, decimal_places=2)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.society.society_name



class Member(models.Model):
    society = models.ForeignKey(Society, related_name='society', on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    starting_share = models.IntegerField(blank=False, null=False)
    starting_loan = models.IntegerField(blank=False, null=False)
    date_of_creation = models.DateTimeField(default=datetime.now)
    month_of_creation = models.IntegerField(default=0)
    active = models.BooleanField(default=1)

    def fill_month(self):
        if self.date_of_creation:
            self.month_of_creation = self.date_of_creation.month


    def __str__(self):
        return self.name

class MonthlyRecord(models.Model):
    MONTH = (
        ('1','January'),
        ('2','February'),
        ('3','March'),
        ('4','April'),
        ('5','May'),
        ('6','June'),
        ('7','July'),
        ('8','August'),
        ('9','September'),
        ('10','October'),
        ('11','November'),
        ('12','December'),
    )


    member = models.ForeignKey(Member, related_name='members', on_delete=models.CASCADE)
    member_name = models.CharField(max_length=1025, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)
    month = models.CharField(choices=MONTH, max_length=20, blank=True, null=True, default=0)
    year = models.IntegerField(blank=True, null=True)
    previous_share = models.IntegerField(blank=True, null=True)
    previous_loan = models.IntegerField(blank=True, null=True)
    share = models.IntegerField(blank=True, null=True)
    total_share = models.IntegerField(blank=True, null=True)
    installment = models.IntegerField(blank=True, null=True)
    installment_filled = models.BooleanField(default=False)
    balance_loan = models.IntegerField(blank=True, null=True)
    interest = models.IntegerField(blank=True, null=True)
    late_fees = models.IntegerField(default=0, blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=30, blank=True, null=True)


    def fill_month(self):
        cur_date = self.date
        month = cur_date.month
        return month
        # print(cur_month, cur_year)

    def fill_year(self):
        cur_date = self.date
        year = cur_date.year
        return year

    def __str__(self):
        return self.member.name
