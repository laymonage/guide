# Generated by Django 4.1.2 on 2022-10-25 10:32

from django.db import migrations


def add_home_page_introduction(apps, schema_editor):
    HomePage = apps.get_model("core", "HomePage")
    HomePage.objects.update(
        introduction=(
            "This documentation is written for anyone creating content "
            "or managing content production in Wagtail. It covers everything "
            "you can expect when using a standard Wagtail site."
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_homepage_introduction"),
    ]

    operations = [
        migrations.RunPython(add_home_page_introduction),
    ]
