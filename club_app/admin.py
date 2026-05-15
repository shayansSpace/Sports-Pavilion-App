from django.contrib import admin
from .models import Member, MembershipPlan, SportsFacility, PlayUnit, MemberPhone# Import all your models

# Registering them makes them visible in the /admin dashboard
admin.site.register(Member)
admin.site.register(MembershipPlan)
admin.site.register(SportsFacility)
admin.site.register(PlayUnit)
admin.site.register(MemberPhone)