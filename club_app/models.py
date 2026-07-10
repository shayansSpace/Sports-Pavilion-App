from django.db import models
# ==========================================
# 1. INDEPENDENT STRONG ENTITIES
# ==========================================

class MembershipPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=100)
    duration_months = models.PositiveIntegerField()
    plan_price = models.DecimalField(max_digits=10, decimal_places=2)
    gym_access = models.BooleanField(default=True)

    @property
    def formatted_id(self):
        return f"P-{self.plan_id:03d}"  # e.g. P-001

    def __str__(self):
        return f"{self.formatted_id} | {self.plan_name}"


class SportsFacility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=100)
    facility_type = models.CharField(max_length=50)
    sp_hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def formatted_id(self):
        return f"F-{self.facility_id:03d}"  # e.g. F-001

    def __str__(self):
        return f"{self.formatted_id} | {self.facility_name}"


class GymEquipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=100)
    ge_brand = models.CharField(max_length=50)
    ge_purchase_date = models.DateField()
    ge_condition = models.CharField(max_length=50)

    @property
    def formatted_id(self):
        return f"E-{self.equipment_id:03d}"  # e.g. E-001

    def __str__(self):
        return f"{self.formatted_id} | {self.equipment_name}"


# ==========================================
# 2. WEAK ENTITY (PLAY_UNIT)
# ==========================================

class PlayUnit(models.Model):
    # Composite PK in the schema: (facility_id, unit_num)
    # Django doesn't natively support composite PKs, so we use a surrogate AutoField
    # and enforce the composite uniqueness constraint below.
    unit_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(SportsFacility, on_delete=models.CASCADE, related_name='units')
    unit_num = models.CharField(max_length=20)
    unit_status = models.CharField(max_length=20, default='Available')

    class Meta:
        unique_together = ('facility', 'unit_num')  # Enforces weak entity composite key

    @property
    def formatted_id(self):
        return f"U-{self.unit_id:03d}"  # e.g. U-001

    def __str__(self):
        return f"{self.facility.facility_name} --- {self.unit_num} [{self.unit_status}]"


# ==========================================
# 3. PEOPLE & SPECIALIZATION
# ==========================================

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    # Composite attribute (staff_name) flattened into two fields:
    staff_first_name = models.CharField(max_length=50)
    staff_last_name = models.CharField(max_length=50)
    staff_role = models.CharField(max_length=50)
    staff_salary = models.DecimalField(max_digits=10, decimal_places=2)

    # M:N Relationship — MAINTAINS (Staff ↔ SportsFacility)
    maintains_facilities = models.ManyToManyField(SportsFacility, blank=True, related_name='maintained_by_staff')

    @property
    def formatted_id(self):
        return f"S-{self.staff_id:03d}"  # e.g. S-001

    @property
    def full_name(self):
        return f"{self.staff_first_name} {self.staff_last_name}"

    def __str__(self):
        return f"{self.formatted_id} | {self.full_name} ({self.staff_role})"


class GymTrainer(Staff):
    # ISA Specialization — Django auto-creates a 1:1 link back to Staff (staff_ptr_id)
    # Inherited fields: staff_id, staff_name, staff_salary, staff_role, phones
    # Specific fields below:
    trainer_start_time = models.TimeField()
    trainer_end_time = models.TimeField()

    @property
    def formatted_id(self):
        return f"T-{self.staff_id:03d}"  # e.g. T-001 (trainers get T prefix)

    def __str__(self):
        return f"{self.formatted_id} | {self.full_name} (Trainer)"


class Visitor(models.Model):
    visitor_id = models.AutoField(primary_key=True)
    # Composite attribute (vis_name) flattened:
    vis_first_name = models.CharField(max_length=50)
    vis_last_name = models.CharField(max_length=50)
    visit_date = models.DateField(auto_now_add=True)

    @property
    def formatted_id(self):
        return f"V-{self.visitor_id:03d}"  # e.g. V-001

    @property
    def full_name(self):
        return f"{self.vis_first_name} {self.vis_last_name}"

    def __str__(self):
        return f"{self.formatted_id} | {self.full_name}"


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    # SUBSCRIBES relationship (N:1 Member → MembershipPlan)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    # Composite attribute (mem_name) flattened:
    mem_first_name = models.CharField(max_length=50)
    mem_last_name = models.CharField(max_length=50)
    mem_email = models.EmailField(unique=True)
    mem_join_date = models.DateField()

    @property
    def formatted_id(self):
        return f"M-{self.member_id:03d}"  # e.g. M-001

    @property
    def full_name(self):
        return f"{self.mem_first_name} {self.mem_last_name}"

    def __str__(self):
        return f"{self.formatted_id} | {self.full_name}"


# ==========================================
# 4. MULTI-VALUED ATTRIBUTES (Separate tables per 1NF)
# ==========================================

class VisitorPhone(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.visitor.formatted_id} → {self.phone_number}"

class MemberPhone(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.member.formatted_id} → {self.phone_number}"


class StaffPhone(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.staff.formatted_id} → {self.phone_number}"


# ==========================================
# 5. TRANSACTIONS — Normalized to 3NF per the document
# ==========================================

class Booking(models.Model):
    """
    3NF version: booking_id, facility_id, unit_num, booking_date,
    bk_start_time, bk_end_time ONLY.
    Member/Visitor links are in separate junction tables below.
    """
    booking_id = models.AutoField(primary_key=True)
    play_unit = models.ForeignKey(
        PlayUnit, on_delete=models.CASCADE, related_name='bookings'
    )
    booking_date = models.DateField()
    bk_start_time = models.TimeField()
    bk_end_time = models.TimeField()

    @property
    def formatted_id(self):
        return f"B-{self.booking_id:03d}"

    def __str__(self):
        return f"{self.formatted_id} | {self.play_unit} [{self.bk_start_time}–{self.bk_end_time}]"


class MemberBooking(models.Model):
    """2NF split: links a Member to a Booking."""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='member_booking')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f"{self.member.formatted_id} → {self.booking.formatted_id}"


class VisitorBooking(models.Model):
    """2NF split: links a Visitor to a Booking."""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='visitor_booking')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f"{self.visitor.formatted_id} → {self.booking.formatted_id}"


class Payment(models.Model):
    """
    3NF version: payment_id, amount, payment_date, payment_method ONLY.
    Member/plan and booking links are in separate tables below.
    """
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    @property
    def formatted_id(self):
        return f"PAY-{self.payment_id:03d}"

    def __str__(self):
        return f"{self.formatted_id} | ${self.amount} via {self.payment_method}"


class MembershipPayment(models.Model):
    """3NF split: links a Payment to a Member + Plan (subscription payment)."""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='membership_payment')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='membership_payments')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"{self.payment.formatted_id} → {self.member.formatted_id} | {self.plan}"


class BookingPayment(models.Model):
    """3NF split: links a Payment to a Booking."""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='booking_payment')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"{self.payment.formatted_id} → {self.booking.formatted_id}"