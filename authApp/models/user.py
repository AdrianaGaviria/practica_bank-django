from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Los usuarios deben tener un nombre de usuario")

        user = self.model(username = username)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username = username,
            password = password
        )
        user.id_admin = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key = True)
    username = models.CharField('Username',max_length = 15,unique = True)
    password = models.CharField('Password',max_length = 255)
    name = models.CharField('Name',max_length = 30)
    email = models.EmailField('Email',max_length = 100)

    def save(self, **kwargs):
        some_salt = 'wqeweasdasd545'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)

    objects = UserManager()
    USERNAME_FIELD = 'username'