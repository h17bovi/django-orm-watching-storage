from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f"{self.owner_name} (inactive)"


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    @property
    def get_duration(self):
        time_in = localtime(self.entered_at)
        if self.leaved_at:
            time_out = localtime(self.leaved_at)
        else:
            time_out = timezone.now().replace(microsecond=0)
        delta = time_out - time_in
        return delta

    @staticmethod
    def format_duration(duration):
        total_seconds = duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}ч {minutes}мин"

    @property
    def is_strange(self, minutes=60):
        visit_in_seconds = self.get_duration.total_seconds()
        visit_in_minutes = visit_in_seconds // 60
        return visit_in_minutes > minutes

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(f"leaved at {self.leaved_at}" if self.leaved_at else "not leaved"),
        )
