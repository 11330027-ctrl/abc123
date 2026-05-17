from django.db import models
from django.core.validators import MinValueValidator

class Device(models.Model):
    DEVICE_TYPES = [
        ('ipad', 'iPad'),
        ('chromebook', 'Chromebook'),
        ('surface_go', 'SurfaceGo'),
        ('acer_laptop', 'Acer筆電'),
    ]
    SCHOOL_SECTIONS = [
        ('junior', '國中部'),
        ('senior', '高中部'),
    ]

    name = models.CharField("載具名稱/編號", max_length=50)
    device_type = models.CharField("載具類型", max_length=20, choices=DEVICE_TYPES)
    section = models.CharField("適用學部", max_length=10, choices=SCHOOL_SECTIONS)
    is_bulk = models.BooleanField("是否為散裝", default=False)
    is_active = models.BooleanField("是否啟用(隱藏/刪除開關)", default=True)

    def __str__(self):
        return f"[{self.get_section_display()}] {self.get_device_type_display()} - {self.name}"


class RentalRecord(models.Model):
    PERIODS = [(i, f"第 {i} 節") for i in range(1, 8)] 

    date = models.DateField("租借日期")
    period = models.IntegerField("節次", choices=PERIODS)
    school_section = models.CharField("學部", max_length=10, choices=Device.SCHOOL_SECTIONS)
    student_name = models.CharField("學生名字", max_length=50)
    student_class = models.CharField("班級", max_length=50)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name="所選載具")
    quantity = models.PositiveIntegerField("借用數量", default=1)

    def __str__(self):
        return f"{self.date} {self.get_period_display()} - {self.student_name}({self.device})"
# Create your models here.
