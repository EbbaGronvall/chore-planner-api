from django.db import models
from django.core.exceptions import ValidationError
from profiles.models import Profile
from django.utils import timezone

# A model for the tasks

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=30)
    description = models.TextField()
    task_giver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='giver_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assigned_to_tasks')

    def clean(self):
        # Validate that due date is not in the past
        if self.due_date < timezone.now().date():
            raise ValidationError('Due date can not be in the past.')

        # Validate that only parents can assign tasks within their household
        

        if self.task_giver.role != 'Parent':
            raise ValidationError('Only parents can assign tasks.')

        if not self.task_giver.household.filter(id__in=self.assigned_to.household.values('id')).exists():
            raise ValidationError('You can only assign tasks to members of the same household as you!')


    def save(self, *args, **kwargs):
        self.full_clean()
        super(Task, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return self.title
