from rest_framework import serializers
from .models import AuthModel

class AuthModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModel
        fields = "__all__"
        extra_kwargs = {"password":{"write_only":True}}

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthModel
        fields = "__all__"

    def create(self, validated_data):
        usr = AuthModel.objects.create(
            username = validated_data["username"],
            email = validated_data["email"]
        )
        usr.savePassword(validated_data["password"])
        usr.save()
        return usr
    
# It is not a ModelSerializer it is a serializer for Login so class Meta is not needed and serializers.ModelSerializer is also not needed serializer.Serializer.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()