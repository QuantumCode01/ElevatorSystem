from django.db import models

# Create your models here.
class elevator(models.Model):
    direction = (
        ("Up", "Up"),
        ("Down", "Down"),
        ("Idle", "Idle"),
      )
    
    door_status=(
      ("Close","Close"),
      ("Open","Open"),
    )
    elevator_id=models.IntegerField()
    current_floor=models.IntegerField()
    operational=models.BooleanField(default=True)
    direction=models.CharField(max_length=10, choices=direction,default="Idle")
    is_busy = models.BooleanField(default=False)
    door=models.CharField(max_length=10,choices=door_status,default="Close")
    
    def __str__(self):
        return str(self.elevator_id)
      
class Person(models.Model):
  elevator=models.ForeignKey(elevator, on_delete=models.CASCADE,null=True)
  requesting_floor=models.IntegerField()
  destination_floor=models.IntegerField(null=True)


