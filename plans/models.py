from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.shortcuts import reverse, redirect


class UsersPlans(models.Model):
    ''' All plans belonging to the user '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    plans = models.ManyToManyField('Plan', blank=True)

    def __str__(self):
        return self.user.username

    def plans_list(self):
        return self.plans.all()

    class Meta:
        verbose_name = "User's Plans"
        verbose_name_plural = "User's Plans"

# Use a signal to create an instance on signup
def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    if created:
        UsersPlans.objects.get_or_create(user=instance)

# ...and link it
post_save.connect(post_user_signup_receiver, sender=settings.AUTH_USER_MODEL)

class Coach(models.Model):
    ''' Coachs create the Plans '''
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = 'Coaches'


class Plan(models.Model):
    ''' Plans are available for purchase '''
    title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField()
    slug = models.SlugField()
    image = models.ImageField()
    price = models.FloatField()
    plan_id = models.CharField(max_length=10)
    created_by = models.ManyToManyField(Coach)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("plans:plan-details", kwargs={
            'slug': self.slug
        })


class Section(models.Model):
    ''' Plans are divided into sections '''
    title = models.CharField(max_length=150)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    section_number = models.IntegerField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("plans:section-details", kwargs={
            'plan_slug': self.plan.slug,
            'section_number': self.section_number
        })


class Activity(models.Model):
    ''' Sections contain user activities / todos '''
    title = models.CharField(max_length=150)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    activity_number = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("plans:activity-details", kwargs={
            'plan_slug': self.section.plan.slug,
            'section_number': self.section.section_number,
            'activity_number': self.activity_number
        })

    class Meta:
        verbose_name_plural = 'Activities'


class Example(models.Model):
    ''' Examples of completed activities '''
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    example_number = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return f"{self.activity.title}-{self.pk}"


