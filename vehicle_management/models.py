from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


# Create your models here.
def validate_model_year(value):
    current_year = datetime.datetime.now().year
    if value >= current_year:
        raise ValidationError(
            _('%(value)s is not a valid model year. It should be less than the current year.'),
            params={'value': value},
        )


class VehicleDetails(models.Model):
    car_model = models.CharField(max_length=220)
    chassis_number = models.CharField(max_length=100, unique=True)
    model_year = models.IntegerField(default=2000, validators=[validate_model_year])
    shape = models.CharField(max_length=4)
    auction_grade = models.CharField(max_length=200)
    package = models.TextField()
    color = models.CharField(max_length=20)
    mileage = models.DecimalField(max_digits=10, decimal_places=2)
    cc = models.DecimalField(max_digits=10, decimal_places=2)
    seat_capacity = models.IntegerField(default=1)
    origin_country = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.chassis_number


STATUS_CHOICES = [
    ('Empty', 'Empty'),
    ('Port', 'Port'),
    ('Onship', 'Onship'),
    ('Inhouse', 'Inhouse'),
    ('Workshop', 'Workshop'),
    ('Other', 'Other'),
]


class VehicleSeries(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.slug = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class VehicleAvailability(models.Model):
    series = models.ForeignKey(VehicleSeries, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_details = models.OneToOneField(VehicleDetails, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Empty')
    port_location = models.CharField(max_length=200, null=True, blank=True)
    shed_number = models.TextField(null=True, blank=True)
    onship = models.TextField(null=True, blank=True)
    inhouse_address = models.TextField(null=True, blank=True)
    workshop_address = models.TextField(null=True, blank=True)
    other_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.series.name} & {self.vehicle_details.chassis_number}"


class VehiclePrice(models.Model):
    series = models.ForeignKey(VehicleSeries, on_delete=models.CASCADE, null=True, blank=True)
    posting_date = models.DateField(auto_now_add=True)
    vehicle_details = models.OneToOneField(VehicleDetails, on_delete=models.CASCADE, null=True, blank=True)
    currency = models.CharField(max_length=5, default="$")
    company_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.sale_price = self.company_price + self.customer_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.series} - Vehicle Price"


class OtherVehicleItems(models.Model):
    vehicle_price = models.ForeignKey(VehiclePrice, on_delete=models.CASCADE, related_name='other_items')
    item = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_price.series} - {self.item}"
