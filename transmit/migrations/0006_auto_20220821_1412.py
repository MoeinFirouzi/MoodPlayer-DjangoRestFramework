# Generated by Django 3.2 on 2022-08-21 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transmit", "0005_rename_session_id_musicstate_session"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sensorstate",
            old_name="accelerationLength",
            new_name="acceleration_length",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="accelerationY",
            new_name="acceleration_y",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="accelerationZ",
            new_name="acceleration_z",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="angularVelocityLength",
            new_name="angularVelocity_length",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="angularVelocityX",
            new_name="angularVelocity_x",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="angularVelocityY",
            new_name="angularVelocity_y",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="angularVelocityZ",
            new_name="angularVelocity_z",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="headingMagneticNorth",
            new_name="headingMagnetic_north",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationUpdateTime",
            new_name="locationUpdate_time",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationAccuracy",
            new_name="location_accuracy",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationAltitude",
            new_name="location_altitude",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationAltitudeRefrenceSystem",
            new_name="location_altitude_reference_system",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationCourseTrueNorth",
            new_name="location_course_true_north",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationIsFromMockProvider",
            new_name="location_is_from_mock_provider",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationLatitude",
            new_name="location_latitude",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationLongitude",
            new_name="location_longitude",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationSpeed",
            new_name="location_speed",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="locationVerticalAccuracy",
            new_name="location_vertical_accuracy",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="magneticFieldLength",
            new_name="magneticField_length",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="magneticFieldX",
            new_name="magneticField_x",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="magneticFieldY",
            new_name="magneticField_y",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="magneticFieldZ",
            new_name="magneticField_z",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="orientationIsIdentity",
            new_name="orientation_isIdentity",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="orientationLength",
            new_name="orientation_length",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="orientationW",
            new_name="orientation_w",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="orientationX",
            new_name="orientation_x",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="orientationY",
            new_name="orientation_y",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="orientationZ",
            new_name="orientation_z",
        ),
        migrations.RenameField(
            model_name="sensorstate",
            old_name="pressureHectoPascal",
            new_name="pressure_hecto_pascal",
        ),
    ]
