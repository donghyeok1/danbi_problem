from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from rest_framework.exceptions import ValidationError
from django.core.mail.message import EmailMessage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required=True,
        write_only=True,
        max_length=30
    )
    password = serializers.CharField(
        required=True,
        write_only=True
    )

    # db에서 긁어올 것이 아닌 쓰기 전용, 직렬화시에 해당 데이터를 포함시키지 않음.

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def validate_email(self, value):
        email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not email_regex.match(value):
            raise serializers.ValidationError("이메일 형식이 아닙니다.")
        return email_regex.findall(value)[0]

    def validate_password(self, value):
        password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")

        if not password_regex.match(value):
            raise ValidationError('유저의 비밀번호는 8글자 이상이며 특수문자, 숫자를 포함해야 합니다.')
        return password_regex.findall(value)[0]


    def create(self, validated_data):
        email = validated_data['email']
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            user = User.objects.create_user(**validated_data)
            user.save()
            return user
        else:
            raise serializers.ValidationError('이미 존재하는 회원의 email 입니다.')



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                token = TokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
            else:
                raise serializers.ValidationError("회원 정보가 일치하지 않습니다.")

        results = {
            "email": email,
            "refresh_token": refresh_token,
            "access_token": access_token
        }

        return results
