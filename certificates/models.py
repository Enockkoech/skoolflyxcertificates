from django.db import models
import uuid

class School(models.Model):
    name = models.CharField(max_length=255)
    motto = models.CharField(max_length=255)
    vision_statement = models.TextField()
    logo = models.ImageField(upload_to='school_logos/')

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    certificate_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

# from django.db import models
# import uuid

# class School(models.Model):
#     name = models.CharField(max_length=255)
#     motto = models.CharField(max_length=255)
#     vision_statement = models.TextField()
#     logo = models.ImageField(upload_to='school_logos/')

#     def __str__(self):
#         return self.name

# class Student(models.Model):
#     first_name = models.CharField(max_length=255)
#     second_name = models.CharField(max_length=255)
#     profile_picture = models.ImageField(upload_to='profile_pictures/')
#     school = models.ForeignKey(School, on_delete=models.CASCADE)
#     certificate_number = models.PositiveBigIntegerField(unique=True, editable=False)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.first_name} {self.second_name}'

#     def save(self, *args, **kwargs):
#         if not self.certificate_number:
#             self.certificate_number = uuid.uuid4().int & (1<<63)-1  # Ensure the number is positive and fits in 64 bits
#             while Student.objects.filter(certificate_number=self.certificate_number).exists():
#                 self.certificate_number = uuid.uuid4().int & (1<<63)-1
#         super(Student, self).save(*args, **kwargs)

