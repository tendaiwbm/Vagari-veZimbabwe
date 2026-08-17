from django import forms
from django.core.exceptions import ValidationError


def validate_admin_level_ward(admin_level):
    """Validate that the admin_level provided corresponds to the accepted 
       geographic boundary aggregation level for ward population distribution"""
    
    if admin_level != "ward":
        raise ValidationError(f"{admin_level} is not a valid admin_level for ward population distribution.")

def validate_year(year):
    """Validate that the year provided corresponds to a census year"""
    if year not in [2012,2022]:
        raise ValidationError(f"{year} is not an accepted value.")

def validate_sex(year):
    """Validate that the given sex is male or female"""
    
    if sex:
        if sex not in ["male","female"]:
            raise ValidationError(f"{sex} is not an accepted value.")


class BaseDistributionRequestValidator(forms.Form):
    """Base class for validation of query strings provided in requests for population distribution data"""
    
    admin_level = forms.CharField(max_length=30)
    grain = forms.CharField(max_length=8)
    sex = forms.CharField(max_length=6,validators=[validate_sex])
    year = forms.IntegerField(validators=[validate_year])

    field_order = ["admin_level","grain"]


class WardRequestValidator(BaseDistributionRequestValidator):
    """Validate the query string provided in requests for ward data"""

    def clean_admin_level(self):
        """Validate that the admin_level provided corresponds to the accepted 
           geographic boundary aggregation level for ward population distribution"""
        
        admin_level = self.cleaned_data["admin_level"]
        if admin_level != "ward":
            raise ValidationError(f"{admin_level} is not a valid admin_level for ward population distribution.")

        return admin_level
    
    def clean_grain(self):
        """Custom clean logic to 
           1. check whether admin_level and granularity are in sync.
           2. coerce the granularity where necessary."""
    
        grain = self.cleaned_data.get("grain")
        
        if grain != "ward":
            # log that grain was not as expected, 
            # and that grain will be coerced to expected value
            grain = "ward"

        return grain
