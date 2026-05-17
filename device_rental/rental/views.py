from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Device, RentalRecord
from .forms import RentalForm
from django.db.models import Sum
import datetime

# 前端預約租借頁面
def rental_create_view(render_request):
    if render_request.method == 'POST':
        form = RentalForm(render_request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.date = form.cleaned_data['date']
            record.period = form.cleaned_data['period']
            record.save()
            return render(render_request, 'rental/success.html')
    else:
        form = RentalForm()
    return render(render_request, 'rental/form.html', {'form': form})


# 2. 供前端 JavaScript 呼叫的 API：動態過濾還能借用的載具
def get_available_devices(request):
    section = request.GET.get('section')   # junior or senior
    date_str = request.GET.get('date')
    period = request.GET.get('period')

    if not (section and date_str and period):
        return JsonResponse({'devices': []})

    # 找出該節課已經被借走的「固定載具」ID 列表
    rented_device_ids = RentalRecord.objects.filter(
        date=date_str,
        period=period,
        device__is_bulk=False
    ).values_list('device_id', flat=True)

    # 篩選：未損壞 + 屬於該學部 + 排除了當節已借出的固定載具
    available_devices = Device.objects.filter(
        is_active=True,
        section=section
    ).exclude(id__in=rented_device_ids)

    data = [
        {'id': d.id, 'name': f"{d.get_device_type_display()} - {d.name}", 'is_bulk': d.is_bulk}
        for d in available_devices
    ]
    return JsonResponse({'devices': data})


# 3. 管理員日曆儀表板 (支援切換：日/月/年統計)
def admin_dashboard(request):
    view_type = request.GET.get('view_type', 'day') # day, month, year
    target_date_str = request.GET.get('date', str(datetime.date.today()))
    
    target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d').date()
    records = RentalRecord.objects.all()

    if view_type == 'day':
        records = records.filter(date=target_date)
    elif view_type == 'month':
        records = records.filter(date__year=target_date.year, date__month=target_date.month)
    elif view_type == 'year':
        records = records.filter(date__year=target_date.year)

    # 依每節課/載具統計總租借數
    stats = records.values('period', 'device__device_type', 'device__name').annotate(total_qty=Sum('quantity'))

    context = {
        'stats': stats,
        'view_type': view_type,
        'target_date': target_date,
    }
    return render(request, 'rental/dashboard.html', context)


# Create your views here.
