from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Household(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def clean(self):
        """
        Validates length of name.
        """
        if len(self.name) < 3:
            raise ValidationError({
                'name': 'Household name must be at least 3 characters long.'
                })

    def save(self, *args, **kwargs):
        """
        Saves the household after cleaning and generating a slug.
        """
        self.full_clean()

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
