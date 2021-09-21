from rest_framework import serializers

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

    class Meta:
        model = User
        fields = ("id", "username", "profile")


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


class GroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ("id", "name", "description", "banner_url", "category", "members")

    # TODO: remove if member info is not needed in the response
    def get_members(self, instance):
        records = Membership.objects.filter(group=instance).values_list(
            "user", flat=True
        )
        users = User.objects.filter(pk__in=records)
        return UserSerializer(users, many=True).data


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "description", "banner_url", "category")
