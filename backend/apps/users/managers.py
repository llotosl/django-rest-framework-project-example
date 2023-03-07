from django.contrib.auth.models import UserManager

from typing import Any


class CustomUserManager(UserManager):
    def create_user(self, email:str, password:str, **extra_fields: Any):
        
        if not email:
            raise ValueError('Email must be not None')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email:str, password:str, **extra_fields: Any):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('is_staff or is_superuser field must be True')
        
        return self.create_user(email, password, **extra_fields)