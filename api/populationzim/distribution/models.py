from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


class Ward(models.Model):
    ward_number = models.IntegerField(primary_key=True)
    district_name = models.CharField(max_length=30)
    province_name = models.CharField(max_length=30)

    male_population_2022 = models.IntegerField()
    female_population_2022 = models.IntegerField()
    total_population_2022 = models.IntegerField()
    male_population_2012 = models.IntegerField()
    female_population_2012 = models.IntegerField()
    total_population_2012 = models.IntegerField()

    total_households_2022 = models.IntegerField()
    total_households_2012 = models.IntegerField()
    avg_householdsize_2022 = models.IntegerField()
    avg_householdsize_2012 = models.IntegerField()

    geom = ArrayField(ArrayField(ArrayField(ArrayField(models.DecimalField()))))

    class Meta:
        managed = False
        db_table = f'"{settings.BASE_SCHEMA}"."ward"'
        unique_together = [["ward_number","district_name"]]

    objects = models.Manager()
