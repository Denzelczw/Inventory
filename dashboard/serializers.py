from dashboard.models import Company, Individual
from user.models import Profile
from django.contrib.auth.models import Group, User
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    read_only_fields = ['id', 'created_at', 'updated_at']
    class Meta:
        model = Company
        fields = '__all__'

class IndividualSerializer(serializers.ModelSerializer):
    read_only_fields = ['id', 'created_at', 'updated_at']
    class Meta:
        model = Individual
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'staff', 'address', 'user_type', 'user_company', 'phone', 'image']