# Generated by Django 5.1.4 on 2025-02-13 19:46

import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('Name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Description', models.CharField(max_length=255)),
                ('NutritionalInfo', models.JSONField()),
                ('Category', models.CharField(choices=[('PRODUCE', 'Produce'), ('MEAT', 'Meat'), ('DAIRY', 'Diary'), ('GRAINS', 'Grains'), ('SPICES', 'Spices'), ('CONDIMENTS', 'Condiments'), ('BAKING', 'Baking'), ('BEVERAGES', 'Beverages')], default='PRODUCE', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('RecipeID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=50)),
                ('Description', models.TextField()),
                ('PrepSteps', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), blank=True, size=None)),
                ('Difficulty', models.CharField(choices=[('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard')], max_length=100)),
                ('Gallery', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, size=None)),
                ('Category', models.CharField(max_length=50)),
                ('VideoURL', models.CharField(max_length=200, null=True)),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('Language', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
                ('CookingTime', models.CharField(max_length=50)),
                ('PrepTime', models.CharField(max_length=50)),
                ('DietaryInfo', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('VEGAN', 'Vegan'), ('VEGETARIAN', 'Vegetarian'), ('GLUTEN_FREE', 'Gluten free'), ('DAIRY_FREE', 'Dairy free'), ('NUT_FREE', 'Nut free'), ('LOW_CARB', 'Low carb'), ('LOW_FAT', 'Low fat'), ('HALAL', 'Halal'), ('KOSHER', 'Kosher'), ('PALEO', 'Paleo')], default='VEGAN', max_length=100), blank=True, size=None)),
                ('SeasonalTags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
                ('Keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, size=None)),
                ('PopularityScore', models.FloatField()),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('CommentID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('Content', models.TextField()),
                ('CreatedAt', models.DateTimeField(auto_now=True)),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                ('RecipeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.CharField(max_length=100)),
                ('IngredientName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
                ('RecipeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeNutrition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ServingSize', models.CharField(max_length=100)),
                ('Calories', models.IntegerField()),
                ('Protein', models.FloatField()),
                ('Carbohydrates', models.FloatField()),
                ('Fat', models.FloatField()),
                ('Fiber', models.FloatField()),
                ('Vitamins', models.JSONField()),
                ('Allergens', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('RecipeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeVersions',
            fields=[
                ('VersionID', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('VersionNumber', models.IntegerField()),
                ('Edits', models.TextField()),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
                ('RecipeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
    ]
