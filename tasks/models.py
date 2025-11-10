from django.db import models
from django.core.exceptions import ValidationError
from profiles.models import Profile
from django.utils import timezone


class Task(models.Model):
    """
    Model representing a task assigned to a household member.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=30)
    description = models.TextField()
    task_giver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='giver_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    assigned_to = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='assigned_to_tasks'
    )

    def clean(self):
        """
        Validates the task instance before saving.
        """
        if self.due_date < timezone.now().date():
            raise ValidationError({
                'due_date': 'Due date can not be in the past.'
            })

        if self.task_giver.role != 'Parent':
            raise ValidationError({
                'task_giver': 'Only parents can assign tasks.'
            })

        if self.task_giver.household != self.assigned_to.household:
            raise ValidationError({
                'assigned_to': (
                    'You can only assign tasks to members of the '
                    'same household as you!'
                )
            })

    def save(self, *args, **kwargs):
        """
        Saves the task instance, ensuring full validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta options for the Task model.
        """
        ordering = ['-due_date']

    def __str__(self):
        """
        Returns a string representation of the task.
        """
        return self.title