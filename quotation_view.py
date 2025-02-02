from django.shortcuts import get_object_or_404, render
from pApp.models import quotation  # import โมเดลที่ชื่อ quotation

def quotation_view(request, quotation_number):
    # ดึงข้อมูล Quotation จากฐานข้อมูล
    quotation_data = get_object_or_404(quotation, number=quotation_number)
    
    # ดึงข้อมูล Order ที่เชื่อมโยงกับ Quotation
    orders = quotation_data.orders.all()  # ใช้ related_name สำหรับดึง orders

    # ส่งข้อมูลไปยัง Template
    return render(request, 'quotation_view.html', {'quotation': quotation_data, 'orders': orders})
