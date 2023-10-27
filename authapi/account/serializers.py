from rest_framework import serializers
from account.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields='__all__'
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']

class PasswordChangeSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords did't match")
        user.set_password(password)
        user.save()
        return attrs
    

# password reset logic using email

class SendResetPasswordEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email']

    def validate(self,attrs):
        pass
