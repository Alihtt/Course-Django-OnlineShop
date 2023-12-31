from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password):

        if not phone_number:
            raise ValueError('You must send phone number')
        if not email:
            raise ValueError('You must send email')
        if not full_name:
            raise ValueError('You must send full name')

        user = self.model(phone_number=phone_number,
                          email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.save()
        return user
