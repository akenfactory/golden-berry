from django.db import models
from django.contrib.auth.models import User

class Search(models.Model):
    area = models.IntegerField()
    prompt = models.CharField(max_length=500)
    updated = models.DateTimeField(auto_now=True)

# Define the Plan model.
class Plan(models.Model):
    name = models.CharField(max_length=50, default="")
    updated = models.DateTimeField(auto_now=True)
    
# Define the Profile model.
class Profile(models.Model):
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

# Define the Framework model.
class Framework(models.Model):
    name = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)

# Define the Domain model with one to more relationship to ServiceStatus.
class Domain(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

# Define the Area model.
class Area(models.Model):
    name = models.CharField(max_length=50, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()

# Define the ServiceStatus model.
class Service(models.Model):
    name = models.CharField(max_length=50, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()
    Area = models.ForeignKey(Area, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=500, default='')

# Define the Framework model.
class PlanXService(models.Model):
    Plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    Service = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(max_length=200, default='')
    limit = models.IntegerField(default=0)
    def __str__(self):
        display = f"""ID: {self.id} - Plan: {self.Plan.name} - Service: {self.Service.name} - Price: {self.price} - Limit: {self.limit}"""
        return display

# Define the ProfileServices model.
class ProfileServices(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    PlanXService = models.ForeignKey(PlanXService, on_delete=models.CASCADE, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()

# Define the Framework model.
class FrameworkXService(models.Model):
    Framework = models.ForeignKey(Framework, on_delete=models.CASCADE)
    Service = models.ForeignKey(Service, on_delete=models.CASCADE, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()
    
# Define the ServiceStatus model.
class ServiceStatus(models.Model):
    state = models.CharField(max_length=50)
    registered = models.DateTimeField()
    usage = models.IntegerField()
    period = models.CharField(max_length=50)
    payment = models.CharField(max_length=50)
    activity = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    serviceState = models.BooleanField()
    updated = models.DateTimeField(auto_now=True)
    Domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=1)
    ProfileServices = models.ForeignKey(ProfileServices, on_delete=models.CASCADE, default=1)

# Create history model.
class History(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    search = models.CharField(max_length=200)
    result = models.CharField(max_length=1000)
    area = models.IntegerField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    completion_tokens = models.IntegerField(default=0)
    prompt_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    def __str__(self):
        return self.id

# Create the Consumption model.
class Consumption(models.Model):
    request_count = models.IntegerField(default=0)
    Domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=1)
    ProfileServices = models.ForeignKey(ProfileServices, on_delete=models.CASCADE, default=1)

# Create history model.
class TmpHistory(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    search = models.CharField(max_length=200)
    result = models.CharField(max_length=1000)
    area = models.IntegerField()
    guest_ip = models.CharField(max_length=1000)
    guest_attemps = models.IntegerField()
    completion_tokens = models.IntegerField(default=0)
    prompt_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    def __str__(self):
        return self.id

# Create user engine model.
class UserEngine(models.Model):
    path = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)

# Create concept observer model.
class ConceptObserver(models.Model):
    concept = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField()
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    json_content = models.JSONField(blank=True, null=True, default=None)
    concept_properties = models.CharField(max_length=300, default="")
    title = models.CharField(max_length=100, default="")