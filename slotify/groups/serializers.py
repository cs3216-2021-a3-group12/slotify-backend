from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from authentication.models import User, Profile
from groups.models import Group, Category, Tag, Membership


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """

    class Meta:
        model = Profile
        fields = ("student_number", "nusnet_id", "telegram_handle")


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    is_admin = ReadOnlyField()
    is_approved = ReadOnlyField()
    tag = ReadOnlyField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "profile",
            "is_admin",
            "is_approved",
            "tag",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            "id",
            "user",
            "group",
            "is_approved",
            "is_admin",
            "tag",
        )


class MembershipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            "is_approved",
            "is_admin",
            "tag",
        )


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            "user",
            "group",
        )


class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "banner_url")


class GroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    members = serializers.SerializerMethodField()
    is_admin = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "description",
            "banner_url",
            "category",
            "members",
            "is_admin",
            "status",
        )

    def get_members(self, instance):
        records = Membership.objects.filter(group=instance).values_list(
            "user", flat=True
        )
        users = User.objects.filter(pk__in=records)
        for user in users:
            record = Membership.objects.filter(user=user, group=instance).first()
            user.is_admin = record.is_admin
            user.is_approved = record.is_approved
            user.tag = record.tag.name if record.tag is not None else ""
        return UserSerializer(users, many=True).data


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "description", "banner_url", "category")
