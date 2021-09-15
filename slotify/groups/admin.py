from django.contrib import admin
from groups.models import Group, Tag, Category, Membership

admin.site.register(Group)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Membership)