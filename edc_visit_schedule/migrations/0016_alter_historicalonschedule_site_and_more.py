# Generated by Django 5.0 on 2024-01-24 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_visit_schedule", "0015_historicalonschedule_offschedule_onschedule"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalonschedule",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AlterField(
            model_name="offschedule",
            name="site",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AlterField(
            model_name="onschedule",
            name="site",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AlterField(
            model_name="subjectschedulehistory",
            name="site",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
    ]
