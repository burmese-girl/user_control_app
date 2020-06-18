from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class UserProfile(models.Model):

	user = models.OneToOneField(User,on_delete=models.CASCADE)
	phone_num= models.CharField(max_length=11,blank=True,help_text=_("Phone Number"))
	dob=models.CharField(max_length=20,blank=True,help_text='Date of Birth')
	gender=models.CharField(max_length=10,blank=True,help_text="Gender")
	country_code = models.CharField(max_length=6, blank=True, help_text=_('Country Code'))

	def __str__(self):
		return self.user.first_name

User.profile = property (lambda u: UserProfile.objects.get_or_create(user=u))