from django import forms
from django.core.exceptions import ValidationError


def validate_year(year):
    """Validate that the year provided corresponds to a census year"""
    
    if year not in [2012,2022]:
        raise ValidationError(f"{year} is not an accepted value.")

def validate_sex(sex):
    """Validate that the given sex is male or female"""
    
    if sex not in ["male","female","total"]:
        raise ValidationError(f"{sex} is not an accepted value.")

def validate_apply_filter(value):
    """Validate that the given sex is male or female"""
    
    if not isinstance(value,bool) or value not in [True,False]:
        raise ValidationError(f"Value for apply_filter is not an accepted value.")

def validate_admin_names_level(admin_level):
    """Validate that admin level can be used to retrieve unique list of names"""

    if admin_level not in ["province","district"]:
        raise ValidationError(f"'{admin_level}' is not an accepted value for retrieving admin names.")


class BaseDistributionRequestValidator(forms.Form):
    """Base class for validation of query strings provided in requests for population distribution data"""
    
    admin_level = forms.CharField(max_length=30)
    sex = forms.CharField(max_length=6,validators=[validate_sex],empty_value="total")
    year = forms.IntegerField(validators=[validate_year])
    apply_filter = forms.BooleanField(required=False,validators=[validate_apply_filter])
    filter_district = forms.CharField(required=False)
    filter_province = forms.CharField(required=False)

    def clean(self):
        
        data = super().clean()
        
        if data["apply_filter"]:
            if data["filter_district"]:
               data["filter_district"] = data["filter_district"].split(",")
            elif data["filter_province"]:
                data["filter_province"] = data["filter_province"].split(",")
            else:
                raise ValidationError(f"Filter request for ward population distribution incomplete.")
        
        return data


class WardRequestValidator(BaseDistributionRequestValidator):
    """Validate the query string provided in requests for ward data"""

    def clean_admin_level(self):
        """Validate that the admin_level provided corresponds to the accepted 
           geographic boundary aggregation level for ward population distribution"""
         
        admin_level = self.cleaned_data["admin_level"]
        if admin_level != "ward":
            raise ValidationError(f"{admin_level} is not a valid admin_level for ward population distribution.")

        return admin_level
    

class DistrictRequestValidator(BaseDistributionRequestValidator):
    """Validate the query string provided in requests for district data"""

    def clean_admin_level(self):
        """Validate that the admin_level provided corresponds to the accepted 
           geographic boundary aggregation level for district population distribution"""
         
        admin_level = self.cleaned_data["admin_level"]
        if admin_level != "district":
            raise ValidationError(f"'{admin_level}' is not a valid admin_level for district population distribution.")

        return admin_level
    

class ProvinceRequestValidator(BaseDistributionRequestValidator):
    """Validate the query string provided in requests for provincial data"""

    def clean_admin_level(self):
        """Validate that the admin_level provided corresponds to the accepted 
           geographic boundary aggregation level for province population distribution"""
         
        admin_level = self.cleaned_data["admin_level"]
        if admin_level != "province":
            raise ValidationError(f"'{admin_level}' is not a valid admin_level for province population distribution.")

        return admin_level
    

class AdminNamesRequestValidator(forms.Form):
    """Validate the query string provided in requests for provincial data"""

    admin_level = forms.CharField(validators=[validate_admin_names_level])
