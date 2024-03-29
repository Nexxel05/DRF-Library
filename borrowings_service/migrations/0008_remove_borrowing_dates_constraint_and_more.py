# Generated by Django 4.0.2 on 2023-03-06 11:34

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('borrowings_service', '0007_remove_borrowing_dates_constraint_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='borrowing',
            name='dates_constraint',
        ),
        migrations.AddConstraint(
            model_name='borrowing',
            constraint=models.CheckConstraint(check=models.Q(('borrow_date__lte', django.db.models.expressions.F('expected_return_date'))), name='borrow_date_lte_expected_return_date'),
        ),
        migrations.AddConstraint(
            model_name='borrowing',
            constraint=models.CheckConstraint(check=models.Q(('borrow_date__lte', django.db.models.expressions.F('actual_return_date'))), name='borrow_date_lte_actual_return_date'),
        ),
    ]
