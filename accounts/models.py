from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def  create_user(self, first_name, last_name, username, email, phone_no, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an user name address')
        user =  self.model (
            email = self.normalize_email(email),
            first_name =  first_name,
            last_name = last_name,
            username = username,
            phone_no = phone_no,
            )
       
       
        user.set_password(password)  
        user.save(using=self._db)
        return user   

    def  create_superuser(self, first_name, last_name, username, phone_no, email,  password=None):
       
        user =  self.create_user(
            email = self.normalize_email(email),
            first_name =  first_name,
            last_name = last_name,
            username = username,
            password = password,
            phone_no = phone_no,
            )
        user.is_admin = True 
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True  
        user.save(using=self._db)
        return user


class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_no = models.CharField(max_length=50, unique=True)
    
    date_of_joining = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_no']
 
 
    objects = MyAccountManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
   
       
       
    def __str__(self): 
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    
class UserProfile(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    
    def __str__(self): 
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1 } {self.address_line_2}'    
