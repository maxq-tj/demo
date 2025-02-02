from django.shortcuts import get_object_or_404, render
from pApp.models import quotation

def depositslip(request, quotation_number):
    # ดึงข้อมูล quotation ที่ตรงกับ quotation_number
    quotation_data = get_object_or_404(quotation, number=quotation_number)
    
    # ดึงข้อมูล depositslip ที่เกี่ยวข้องกับ quotation
    depositslip_data = quotation_data.depositslips.all()
    
    # ดึงข้อมูล quotations ทั้งหมด
    all_quotations = quotation.objects.all()

    # ส่งข้อมูลทั้งหมดไปยังเทมเพลต
    return render(request, 'depositslipmanage.html', {
        'quotation_number': quotation_data, 
        'depositslips': depositslip_data,
        'quotations': all_quotations
    })
