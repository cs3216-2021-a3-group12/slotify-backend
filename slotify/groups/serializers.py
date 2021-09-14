from rest_framework import serializers

from authentication.models import User
from groups.models import Group, Category, Tag, Membership

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=True)

    class Meta:
        model = Membership
        fields = ("id", "user", "group")


class GroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ("id", "name", "description", "banner_url", "category", "members")

    def get_members(self, instance):
        records = Membership.objects.filter(group=instance).values_list('user', flat=True)
        users = User.objects.filter(pk__in = records)
        return UserSerializer(users, many=True).data

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "description", "banner_url", "category")
