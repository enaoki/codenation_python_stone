from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50)

class User(models.Model):
    name = models.CharField(max_length=50)
    last_login = models.DateField()
    email = models.CharField(max_length=254, validators=[validate_email])
    password = models.CharField(max_length=50, validators=[MinLengthValidator(8)])
    #groups = models.ManyToManyField(Group, verbose_name="list of groups", db_table="api_groupuser")

class Agent(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    env = models.CharField(max_length=20)
    version = models.CharField(max_length=5)
    address = models.CharField(max_length=39, validators=[validate_ipv4_address])

class Event(models.Model):
    LEVEL_CHOICES = [
        (CRITICAL, 'Critical'),
        (DEBUG, 'Debug'),
        (ERROR, 'Error'),
        (WARNING, 'Warning'),
        (INFO, 'Info'),
    ]
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=INFO)
    data = models.TextField()
    arquivado = models.BooleanField(default=True)
    date = models.DateField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)