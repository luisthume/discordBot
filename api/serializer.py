from rest_framework import serializers
from .models import (DiscordUser, Hour)
import requests


class DiscordUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordUser
        fields = ('id',
                  'code',
                  'name',
                  )


class HourSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    discorduser = DiscordUserSerializer()

    class Meta:
        model = Hour
        fields = ('id',
                  'discorduser',
                  'code',
                  'minutes',
                  )

    def get_code(self, instance):
        user_id = instance.discorduser.id
        try:
            obj_user = DiscordUser.objects.get(id=user_id)
            return obj_user.code
        except Exception as e:
            return None