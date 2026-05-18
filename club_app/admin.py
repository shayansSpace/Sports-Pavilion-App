from django.contrib import admin
from .models import Booking, Member, MembershipPlan, SportsFacility, PlayUnit, MemberPhone, VisitorBooking# Import all your models

# Registering them makes them visible in the /admin dashboard
admin.site.register(Member)
admin.site.register(MembershipPlan)
admin.site.register(SportsFacility)
admin.site.register(PlayUnit)
admin.site.register(MemberPhone)
admin.site.register(Booking)
admin.site.register(VisitorBooking)