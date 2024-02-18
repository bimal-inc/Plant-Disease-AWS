from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Detection
from .models import PlantImage



User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password', 'password2', 'bio', 'profile_photo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if both passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        # Remove password2 from the validated data
        validated_data.pop('password2', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            bio=validated_data.get('bio', ''),
            profile_photo=validated_data.get('profile_photo')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'bio', 'profile_photo']




class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['image']


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'bio', 'profile_photo']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'full_name': {'required': False},
            'bio': {'required': False},
            'profile_photo': {'required': False},
        }

    def validate_password(self, value):
        """
        Hash password if it's provided.
        """
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)

        # Check if password is provided and hash it
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = '__all__'  # Specify the fields you want to include, or use '__all__' to include all fields