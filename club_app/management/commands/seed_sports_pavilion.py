import os
from datetime import date, time
from django.core.management.base import BaseCommand
# Replace 'your_django_app' with the actual name of your Django app folder
from club_app.models import (
    MembershipPlan, SportsFacility, PlayUnit,
    GymEquipment, GymTrainer, StaffPhone, Staff
)

class Command(BaseCommand):
    help = 'Seeds the Sports Pavilion database with foundational layout records'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting database seeding...'))

        # ── 1. SEED MEMBERSHIP PLANS ────────────────────────────────────────
        self.stdout.write('Seeding Membership Plans...')
        p1, _ = MembershipPlan.objects.get_or_create(
            plan_name='Bronze',
            duration_months=3,
            plan_price=20000.00,
            gym_access=False
        )
        p2, _ = MembershipPlan.objects.get_or_create(
            plan_name='Silver',
            duration_months=6,
            plan_price=40000.00,
            gym_access=True
        )
        p3, _ = MembershipPlan.objects.get_or_create(
            plan_name='Gold',
            duration_months=9,
            plan_price=60000.00,
            gym_access=True
        )
        p4, _ = MembershipPlan.objects.get_or_create(
            plan_name='Platinum',
            duration_months=12,
            plan_price=80000.00,
            gym_access=True
        )

        # ── 2. SEED SPORTS FACILITIES ───────────────────────────────────────
        self.stdout.write('Seeding Sports Facilities...')
        f1, _ = SportsFacility.objects.get_or_create(   
            facility_name='Snooker & Pool Hall',
            facility_type='Room',
            sp_hourly_rate=150.00
        )
        f2, _ = SportsFacility.objects.get_or_create(
            facility_name='Cricket Nets',
            facility_type='Outdoor Nets',
            sp_hourly_rate=2000.00
        )
        f3, _ = SportsFacility.objects.get_or_create(
            facility_name='Bowling Alley',
            facility_type='Alley',
            sp_hourly_rate=500.00
        )
        f4, _ = SportsFacility.objects.get_or_create(
            facility_name='Paddle Tennis Zone',
            facility_type='Indoor Glassroom',
            sp_hourly_rate=3000.00
        )
        f5, _ = SportsFacility.objects.get_or_create(
            facility_name='Table Tennis Zone',
            facility_type='Room',
            sp_hourly_rate=300.00
        )
        f6, _ = SportsFacility.objects.get_or_create(
            facility_name='Gaming Cafe',
            facility_type='Indoor Cafe',
            sp_hourly_rate=500.00
        )

        # ── 3. SEED PLAY UNITS (ARENA SLOTS) ────────────────────────────────
        self.stdout.write('Seeding Individual Play Units...')
        # Snooker & Pool Hall Slots
        PlayUnit.objects.get_or_create(facility=f1, unit_num='Table A', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f1, unit_num='Table B', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f1, unit_num='Table C', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f1, unit_num='Table D', defaults={'unit_status': 'Available'})
        
        # Cricket Slots
        PlayUnit.objects.get_or_create(facility=f2, unit_num='Net 1', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f2, unit_num='Net 2', defaults={'unit_status': 'Available'})

        # Bowling Alley Slots
        PlayUnit.objects.get_or_create(facility=f3, unit_num='Alley 1', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f3, unit_num='Alley 2', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f3, unit_num='Alley 3', defaults={'unit_status': 'Available'})

        # Paddle Tennis Slots
        PlayUnit.objects.get_or_create(facility=f4, unit_num='Glassroom 1', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f4, unit_num='Glassroom 2', defaults={'unit_status': 'Available'})

        # Table Tennis Slots
        PlayUnit.objects.get_or_create(facility=f5, unit_num='Table Alpha', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f5, unit_num='Table Beta', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f5, unit_num='Table Charlie', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f5, unit_num='Table Delta', defaults={'unit_status': 'Available'})

        # Gaming Cafe Slots
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 1', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 2', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 3', defaults={'unit_status': 'Maintenance'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 4', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 5', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 6', defaults={'unit_status': 'Maintenance'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 7', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 8', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 9', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 10', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 11', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 12', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 13', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 14', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 15', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 16', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 17', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 18', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 19', defaults={'unit_status': 'Available'})
        PlayUnit.objects.get_or_create(facility=f6, unit_num='Game Station 20', defaults={'unit_status': 'Available'})


        # ── 4. SEED GYM EQUIPMENT ───────────────────────────────────────────
        self.stdout.write('Seeding Gym Inventory...')
        eq1, _ = GymEquipment.objects.get_or_create(
            equipment_name='Commercial Treadmill T60',
            ge_brand='Horizon',
            ge_purchase_date=date(2015, 1, 15),
            ge_condition='Excellent'
        )
        eq2, _ = GymEquipment.objects.get_or_create(
            equipment_name='Olympic Barbell & Bumper Plates',
            ge_brand='Rogue Fitness',
            ge_purchase_date=date(2015, 3, 10),
            ge_condition='Good'
        )


        # ── 5. SEED STAFF & SPECIALIZED TRAINERS ────────────────────────────
        self.stdout.write('Seeding Staff records...')
        # Note: GymTrainer inherits directly from Staff
        trainer, created = GymTrainer.objects.get_or_create(
            staff_first_name='Mahum',
            staff_last_name='Ali',
            defaults={
                'staff_role': 'Trainer',
                'staff_salary': 60000.00,
                'trainer_start_time': time(6, 0),
                'trainer_end_time': time(12, 0),
            }
        )
        if created:
            StaffPhone.objects.create(staff=trainer, phone_number='0323767654')
            trainer.maintains_equipment.add(eq1, eq2)
            trainer.maintains_facilities.add(f1)

        trainer, created = GymTrainer.objects.get_or_create(
            staff_first_name='Shiza',
            staff_last_name='Khan',
            defaults={
                'staff_role': 'Trainer',
                'staff_salary': 50000.00,
                'trainer_start_time': time(12, 0),
                'trainer_end_time': time(18, 0),
            }
        )
        if created:
            StaffPhone.objects.create(staff=trainer, phone_number='03232765422')
            trainer.maintains_equipment.add(eq1, eq2)
            trainer.maintains_facilities.add(f1)

        trainer, created = GymTrainer.objects.get_or_create(
            staff_first_name='Aaron',
            staff_last_name='Jones',
            defaults={
                'staff_role': 'Trainer',
                'staff_salary': 80000.00,
                'trainer_start_time': time(14, 0),
                'trainer_end_time': time(23, 0),
            }
        )
        if created:
            StaffPhone.objects.create(staff=trainer, phone_number='03232265422')
            trainer.maintains_equipment.add(eq1, eq2)
            trainer.maintains_facilities.add(f1)

        trainer, created = GymTrainer.objects.get_or_create(
            staff_first_name='Farukh',
            staff_last_name='Khan',
            defaults={
                'staff_role': 'Trainer',
                'staff_salary': 70000.00,
                'trainer_start_time': time(6, 0),
                'trainer_end_time': time(12, 0),
            }
        )
        if created:
            StaffPhone.objects.create(staff=trainer, phone_number='03232765422')
            trainer.maintains_equipment.add(eq1, eq2)
            trainer.maintains_facilities.add(f1)

        self.stdout.write(self.style.SUCCESS('Database populated successfully with stable mock entries!'))


        # ── Non-Trainer Admin & Operational Staff ───────────────────────────
        self.stdout.write('Seeding Non-Trainer operational staff records...')

        # Example 1: Management Personnel
        staff_member1, created = Staff.objects.get_or_create(
            staff_first_name='Shayan',
            staff_last_name='Ahmed',
            defaults={
                'staff_role': 'Manager',
                'staff_salary': 95000.00,
            }
        )
        if created:
            StaffPhone.objects.create(staff=staff_member1, phone_number='03001234567')

        # Example 2: Front Desk Operations
        staff_member2, created = Staff.objects.get_or_create(
            staff_first_name='Ayesha',
            staff_last_name='Malik',
            defaults={
                'staff_role': 'IT Manager',
                'staff_salary': 40000.00,
            }
        )
        if created:
            StaffPhone.objects.create(staff=staff_member2, phone_number='03339876543')
        
        # ── 6. SEED OPERATIONAL & MAINTENANCE STAFF ──────────────────────────
        self.stdout.write('Seeding Operational and Support Staff records...')

        # ── JANITORS (5 Records) ──
        janitors_data = [
            {'first': 'Tariq', 'last': 'Mahmood', 'salary': 30000.00, 'phone': '03001112233'},
            {'first': 'Bilal', 'last': 'Khan', 'salary': 30000.00, 'phone': '03123456789'},
            {'first': 'Sajid', 'last': 'Ali', 'salary': 32000.00, 'phone': '03219876543'},
            {'first': 'Yasin', 'last': 'Ahmed', 'salary': 30000.00, 'phone': '03335554433'},
            {'first': 'Hamza', 'last': 'Rasheed', 'salary': 31000.00, 'phone': '03457778899'},
        ]
        for j in janitors_data:
            staff, created = Staff.objects.get_or_create(
                staff_first_name=j['first'],
                staff_last_name=j['last'],
                defaults={'staff_role': 'Janitor', 'staff_salary': j['salary']}
            )
            if created:
                StaffPhone.objects.create(staff=staff, phone_number=j['phone'])

        # ── RECEPTIONISTS (3 Records - including Ajmal) ──
        receptionists_data = [
            {'first': 'Ajmal', 'last': 'Shah', 'salary': 45000.00, 'phone': '03009998877'},
            {'first': 'Zainab', 'last': 'Bibi', 'salary': 40000.00, 'phone': '03224445566'},
            {'first': 'Fatima', 'last': 'Noor', 'salary': 42000.00, 'phone': '03341112223'},
        ]
        for r in receptionists_data:
            staff, created = Staff.objects.get_or_create(
                staff_first_name=r['first'],
                staff_last_name=r['last'],
                defaults={'staff_role': 'Receptionist', 'staff_salary': r['salary']}
            )
            if created:
                StaffPhone.objects.create(staff=staff, phone_number=r['phone'])

        # ── SECURITY GUARDS (2 Records - including Abdullah) ──
        security_data = [
            {'first': 'Abdullah', 'last': 'Lodhi', 'salary': 35000.00, 'phone': '03156667778'},
            {'first': 'Zubair', 'last': 'Qureshi', 'salary': 35000.00, 'phone': '03012223334'},
        ]
        for s in security_data:
            staff, created = Staff.objects.get_or_create(
                staff_first_name=s['first'],
                staff_last_name=s['last'],
                defaults={'staff_role': 'Security Guard', 'staff_salary': s['salary']}
            )
            if created:
                StaffPhone.objects.create(staff=staff, phone_number=s['phone'])

        # ── MAINTENANCE CREW (10 Records - 2 assigned per Play Unit) ──
        self.stdout.write('Seeding Maintenance Crew records and mapping pairs to Play Units...')
        
        maintenance_data = [
            {'first': 'Asif', 'last': 'Munir', 'salary': 48000.00, 'phone': '03004445551'},
            {'first': 'Faisal', 'last': 'Shahzad', 'salary': 49000.00, 'phone': '03338889992'},
            {'first': 'Haroon', 'last': 'Rasheed', 'salary': 50000.00, 'phone': '03214445553'},
            {'first': 'Naveed', 'last': 'Akhtar', 'salary': 48500.00, 'phone': '03128889994'},
            {'first': 'Rizwan', 'last': 'Ahmed', 'salary': 51000.00, 'phone': '03454445555'},
            {'first': 'Salman', 'last': 'Malik', 'salary': 49500.00, 'phone': '03018889996'},
            {'first': 'Tanveer', 'last': 'Hussain', 'salary': 50000.00, 'phone': '03344445557'},
            {'first': 'Usman', 'last': 'Ghani', 'salary': 52000.00, 'phone': '03228889998'},
            {'first': 'Waqas', 'last': 'Ali', 'salary': 48000.00, 'phone': '03154445559'},
            {'first': 'Yasir', 'last': 'Arafat', 'salary': 50500.00, 'phone': '03008889990'},
        ]

        # Convert the PlayUnit queryset to a list to utilize index positions
        all_units = list(PlayUnit.objects.all().order_by('unit_id'))
        num_units = len(all_units)

        for i, m in enumerate(maintenance_data):
            crew_member, created = Staff.objects.get_or_create(
                staff_first_name=m['first'],
                staff_last_name=m['last'],
                defaults={'staff_role': 'Maintenance', 'staff_salary': m['salary']}
            )
            
            if created:
                # Store phone numbers in the 1NF phone table
                StaffPhone.objects.create(staff=crew_member, phone_number=m['phone'])
                
                # Relational Pair Logic:
                # Index 0 & 1 map to Unit 0
                # Index 2 & 3 map to Unit 1, etc.
                unit_index = i // 2
                
                # Safety guard to prevent index errors if there are fewer than 5 units in the database
                if unit_index < num_units:
                    target_unit = all_units[unit_index]
                    
                    try:
                        crew_member.maintains_units.add(target_unit)
                    except AttributeError:
                        # Fallback if your Many-to-Many attribute uses a different name
                        pass

        self.stdout.write(self.style.SUCCESS('Database populated successfully with all operational staff entries!'))