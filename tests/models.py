from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)

    avatar = models.FileField(upload_to="avatars/", blank=True)
    email = models.EmailField(blank=True, max_length=320, null=True, unique=True)
    phone = models.CharField(max_length=32)

    boolean = models.BooleanField(blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)
    json = models.JSONField(blank=True, null=True)
    positive_integer = models.PositiveIntegerField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    small_integer = models.SmallIntegerField(blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    team = models.ForeignKey("Team", blank=True, null=True, on_delete=models.SET_NULL)
    skills = models.ManyToManyField("Skill", through="RatedSkill")
    tags = models.ManyToManyField("Tag")

    recovery_email = models.EmailField(blank=True, max_length=320, null=True)
    recovery_phone = models.CharField(blank=True, max_length=32, null=True)

    last_active = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    def api(self):
        return dict(id=self.id, email=self.email, phone=self.phone)

    def api_update_fields(self):
        return [
            "id",
            "email",
            "phone",

            "boolean",
            "integer",
            "json",
            "positive_integer",
            "slug",
            "small_integer",

            "recovery_email",

            "last_active",
            "created_at",
        ]


class Role(models.Model):
    name = models.CharField(max_length=100)


class Skill(models.Model):
    name = models.CharField(max_length=200)


class RatedSkill(models.Model):
    class Meta:
        ordering = ["skill__name"]
        unique_together = ["profile", "skill"]

    RATING_CHOICES = [
        (5, "Excellent"),
        (4, "Great"),
        (3, "Average"),
        (2, "Poor"),
        (1, "Bad"),
    ]

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    skill = models.ForeignKey("Skill", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill.name}: {self.get_rating_display()}"


class Tag(models.Model):
    name = models.CharField(max_length=200)


class Team(models.Model):
    name = models.CharField(max_length=100)
