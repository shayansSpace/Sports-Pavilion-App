-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema sports_pavilion
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `auth_group`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `django_content_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label` ASC, `model` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auth_permission`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `content_type_id` INT NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id` ASC, `codename` ASC) VISIBLE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `django_content_type` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 97
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auth_group_permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `group_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id` ASC, `permission_id` ASC) VISIBLE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id` ASC) VISIBLE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `auth_group` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auth_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME(6) NULL DEFAULT NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auth_user_groups`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id` ASC, `group_id` ASC) VISIBLE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id` ASC) VISIBLE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `auth_user_user_permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `permission_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id` ASC, `permission_id` ASC) VISIBLE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id` ASC) VISIBLE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`
    FOREIGN KEY (`permission_id`)
    REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_sportsfacility`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_sportsfacility` (
  `facility_id` INT NOT NULL AUTO_INCREMENT,
  `facility_name` VARCHAR(100) NOT NULL,
  `facility_type` VARCHAR(50) NOT NULL,
  `sp_hourly_rate` DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (`facility_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_playunit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_playunit` (
  `unit_id` INT NOT NULL AUTO_INCREMENT,
  `unit_num` VARCHAR(20) NOT NULL,
  `unit_status` VARCHAR(20) NOT NULL,
  `facility_id` INT NOT NULL,
  PRIMARY KEY (`unit_id`),
  UNIQUE INDEX `club_app_playunit_facility_id_unit_num_efc609dc_uniq` (`facility_id` ASC, `unit_num` ASC) VISIBLE,
  CONSTRAINT `club_app_playunit_facility_id_07dd02b4_fk_club_app_`
    FOREIGN KEY (`facility_id`)
    REFERENCES `club_app_sportsfacility` (`facility_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 36
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_booking` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `booking_date` DATE NOT NULL,
  `bk_end_time` TIME NOT NULL,
  `bk_start_time` TIME NOT NULL,
  `play_unit_id` INT NOT NULL,
  PRIMARY KEY (`booking_id`),
  INDEX `club_app_booking_play_unit_id_a72d4532_fk_club_app_` (`play_unit_id` ASC) VISIBLE,
  CONSTRAINT `club_app_booking_play_unit_id_a72d4532_fk_club_app_`
    FOREIGN KEY (`play_unit_id`)
    REFERENCES `club_app_playunit` (`unit_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_payment` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `amount` DECIMAL(10,2) NOT NULL,
  `payment_date` DATETIME(6) NOT NULL,
  `payment_method` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`payment_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_bookingpayment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_bookingpayment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `booking_id` INT NOT NULL,
  `payment_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `payment_id` (`payment_id` ASC) VISIBLE,
  INDEX `club_app_bookingpaym_booking_id_ce0519e2_fk_club_app_` (`booking_id` ASC) VISIBLE,
  CONSTRAINT `club_app_bookingpaym_booking_id_ce0519e2_fk_club_app_`
    FOREIGN KEY (`booking_id`)
    REFERENCES `club_app_booking` (`booking_id`),
  CONSTRAINT `club_app_bookingpaym_payment_id_83f0d304_fk_club_app_`
    FOREIGN KEY (`payment_id`)
    REFERENCES `club_app_payment` (`payment_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_gymequipment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_gymequipment` (
  `equipment_id` INT NOT NULL AUTO_INCREMENT,
  `equipment_name` VARCHAR(100) NOT NULL,
  `ge_brand` VARCHAR(50) NOT NULL,
  `ge_purchase_date` DATE NOT NULL,
  `ge_condition` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`equipment_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_staff` (
  `staff_id` INT NOT NULL AUTO_INCREMENT,
  `staff_first_name` VARCHAR(50) NOT NULL,
  `staff_last_name` VARCHAR(50) NOT NULL,
  `staff_role` VARCHAR(50) NOT NULL,
  `staff_salary` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`staff_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 27
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_gymtrainer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_gymtrainer` (
  `staff_ptr_id` INT NOT NULL,
  `trainer_start_time` TIME NOT NULL,
  `trainer_end_time` TIME NOT NULL,
  PRIMARY KEY (`staff_ptr_id`),
  CONSTRAINT `club_app_gymtrainer_staff_ptr_id_64c44e7a_fk_club_app_`
    FOREIGN KEY (`staff_ptr_id`)
    REFERENCES `club_app_staff` (`staff_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_gymtrainer_maintains_equipment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_gymtrainer_maintains_equipment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `gymtrainer_id` INT NOT NULL,
  `gymequipment_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `club_app_gymtrainer_main_gymtrainer_id_gymequipme_cc2ba88e_uniq` (`gymtrainer_id` ASC, `gymequipment_id` ASC) VISIBLE,
  INDEX `club_app_gymtrainer__gymequipment_id_ca08aac2_fk_club_app_` (`gymequipment_id` ASC) VISIBLE,
  CONSTRAINT `club_app_gymtrainer__gymequipment_id_ca08aac2_fk_club_app_`
    FOREIGN KEY (`gymequipment_id`)
    REFERENCES `club_app_gymequipment` (`equipment_id`),
  CONSTRAINT `club_app_gymtrainer__gymtrainer_id_119666a2_fk_club_app_`
    FOREIGN KEY (`gymtrainer_id`)
    REFERENCES `club_app_gymtrainer` (`staff_ptr_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_membershipplan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_membershipplan` (
  `plan_id` INT NOT NULL AUTO_INCREMENT,
  `plan_name` VARCHAR(100) NOT NULL,
  `duration_months` INT UNSIGNED NOT NULL,
  `plan_price` DECIMAL(10,2) NOT NULL,
  `gym_access` TINYINT(1) NOT NULL,
  PRIMARY KEY (`plan_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_member` (
  `member_id` INT NOT NULL AUTO_INCREMENT,
  `mem_first_name` VARCHAR(50) NOT NULL,
  `mem_last_name` VARCHAR(50) NOT NULL,
  `mem_email` VARCHAR(254) NOT NULL,
  `mem_join_date` DATE NOT NULL,
  `plan_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`member_id`),
  UNIQUE INDEX `mem_email` (`mem_email` ASC) VISIBLE,
  INDEX `club_app_member_plan_id_e2459af1_fk_club_app_` (`plan_id` ASC) VISIBLE,
  CONSTRAINT `club_app_member_plan_id_e2459af1_fk_club_app_`
    FOREIGN KEY (`plan_id`)
    REFERENCES `club_app_membershipplan` (`plan_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 232
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_memberbooking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_memberbooking` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `booking_id` INT NOT NULL,
  `member_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `booking_id` (`booking_id` ASC) VISIBLE,
  INDEX `club_app_memberbooki_member_id_2a87ffea_fk_club_app_` (`member_id` ASC) VISIBLE,
  CONSTRAINT `club_app_memberbooki_booking_id_e07e6104_fk_club_app_`
    FOREIGN KEY (`booking_id`)
    REFERENCES `club_app_booking` (`booking_id`),
  CONSTRAINT `club_app_memberbooki_member_id_2a87ffea_fk_club_app_`
    FOREIGN KEY (`member_id`)
    REFERENCES `club_app_member` (`member_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_memberphone`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_memberphone` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `phone_number` VARCHAR(15) NOT NULL,
  `member_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `club_app_memberphone_member_id_a33f6d42_fk_club_app_` (`member_id` ASC) VISIBLE,
  CONSTRAINT `club_app_memberphone_member_id_a33f6d42_fk_club_app_`
    FOREIGN KEY (`member_id`)
    REFERENCES `club_app_member` (`member_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_membershippayment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_membershippayment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `member_id` INT NOT NULL,
  `payment_id` INT NOT NULL,
  `plan_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `payment_id` (`payment_id` ASC) VISIBLE,
  INDEX `club_app_membershipp_member_id_6af66cb1_fk_club_app_` (`member_id` ASC) VISIBLE,
  INDEX `club_app_membershipp_plan_id_9e88440d_fk_club_app_` (`plan_id` ASC) VISIBLE,
  CONSTRAINT `club_app_membershipp_member_id_6af66cb1_fk_club_app_`
    FOREIGN KEY (`member_id`)
    REFERENCES `club_app_member` (`member_id`),
  CONSTRAINT `club_app_membershipp_payment_id_40b02345_fk_club_app_`
    FOREIGN KEY (`payment_id`)
    REFERENCES `club_app_payment` (`payment_id`),
  CONSTRAINT `club_app_membershipp_plan_id_9e88440d_fk_club_app_`
    FOREIGN KEY (`plan_id`)
    REFERENCES `club_app_membershipplan` (`plan_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_staff_maintains_facilities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_staff_maintains_facilities` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `staff_id` INT NOT NULL,
  `sportsfacility_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `club_app_staff_maintains_staff_id_sportsfacility__142e663c_uniq` (`staff_id` ASC, `sportsfacility_id` ASC) VISIBLE,
  INDEX `club_app_staff_maint_sportsfacility_id_adaadbe6_fk_club_app_` (`sportsfacility_id` ASC) VISIBLE,
  CONSTRAINT `club_app_staff_maint_sportsfacility_id_adaadbe6_fk_club_app_`
    FOREIGN KEY (`sportsfacility_id`)
    REFERENCES `club_app_sportsfacility` (`facility_id`),
  CONSTRAINT `club_app_staff_maint_staff_id_06a9354b_fk_club_app_`
    FOREIGN KEY (`staff_id`)
    REFERENCES `club_app_staff` (`staff_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_staffphone`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_staffphone` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `phone_number` VARCHAR(15) NOT NULL,
  `staff_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `club_app_staffphone_staff_id_2fde6d17_fk_club_app_staff_staff_id` (`staff_id` ASC) VISIBLE,
  CONSTRAINT `club_app_staffphone_staff_id_2fde6d17_fk_club_app_staff_staff_id`
    FOREIGN KEY (`staff_id`)
    REFERENCES `club_app_staff` (`staff_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 27
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_visitor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_visitor` (
  `visitor_id` INT NOT NULL AUTO_INCREMENT,
  `vis_first_name` VARCHAR(50) NOT NULL,
  `vis_last_name` VARCHAR(50) NOT NULL,
  `visit_date` DATE NOT NULL,
  PRIMARY KEY (`visitor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_visitorbooking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_visitorbooking` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `booking_id` INT NOT NULL,
  `visitor_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `booking_id` (`booking_id` ASC) VISIBLE,
  INDEX `club_app_visitorbook_visitor_id_64acf15d_fk_club_app_` (`visitor_id` ASC) VISIBLE,
  CONSTRAINT `club_app_visitorbook_booking_id_cd8c4eea_fk_club_app_`
    FOREIGN KEY (`booking_id`)
    REFERENCES `club_app_booking` (`booking_id`),
  CONSTRAINT `club_app_visitorbook_visitor_id_64acf15d_fk_club_app_`
    FOREIGN KEY (`visitor_id`)
    REFERENCES `club_app_visitor` (`visitor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `club_app_visitorphone`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `club_app_visitorphone` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `phone_number` VARCHAR(15) NOT NULL,
  `visitor_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `club_app_visitorphon_visitor_id_4f14c968_fk_club_app_` (`visitor_id` ASC) VISIBLE,
  CONSTRAINT `club_app_visitorphon_visitor_id_4f14c968_fk_club_app_`
    FOREIGN KEY (`visitor_id`)
    REFERENCES `club_app_visitor` (`visitor_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `django_admin_log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `action_time` DATETIME(6) NOT NULL,
  `object_id` LONGTEXT NULL DEFAULT NULL,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` SMALLINT UNSIGNED NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  `content_type_id` INT NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id` ASC) VISIBLE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co`
    FOREIGN KEY (`content_type_id`)
    REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `auth_user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `django_migrations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `app` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `applied` DATETIME(6) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `django_session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  INDEX `django_session_expire_date_a5c62663` (`expire_date` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
