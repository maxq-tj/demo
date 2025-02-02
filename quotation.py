from django.http import Http404
from django.shortcuts import render, get_object_or_404
from pApp.models import quotation, order  # เปลี่ยนตามชื่อโมเดลของคุณ

def quotation_view(request, quotation_number):
    try:
        # ดึงข้อมูล Quotation จากฐานข้อมูล โดยใช้หมายเลข quotation_number
        quotation_data = get_object_or_404(quotation, number=quotation_number)
        
        # ดึงข้อมูล orders ที่เกี่ยวข้องกับ quotation นี้
        orders = order.objects.filter(quotation=quotation_data)

        # กำหนด state สำหรับแสดงส่วนที่ต้องการ
        task_state = 'quotation'  # หรือ 'depositslip' ขึ้นอยู่กับสถานะที่ต้องการแสดง
        quotation_data.state = task_state  # กำหนด state ของ quotation

        # ส่งข้อมูลไปยังเทมเพลต
        return render(request, 'quotation.html', {
            'task_state': task_state,
            'quotation': quotation_data,
            'orders': orders,
        })
    except quotation.DoesNotExist:
        # หากไม่พบ Quotation ที่ตรงกับหมายเลข
        raise Http404("Quotation not found")

