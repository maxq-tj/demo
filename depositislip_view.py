from django.shortcuts import render, get_object_or_404
from pApp.models import quotation, depositslip, deposit_orders

def deposit_slip_view(request, quotation_number, depositslip_number):
    # ดึงข้อมูล Quotation
    _quotation = get_object_or_404(quotation, number=quotation_number)
    
    # ดึงข้อมูล DepositSlip
    _depositslip = get_object_or_404(depositslip, depositslip_number=depositslip_number)
    
    # ดึงรายการ DepositOrder ทั้งหมดที่เกี่ยวข้องกับ DepositSlip
    _deposit_orders = deposit_orders.objects.filter(deposit_slip=_depositslip)
    
    # ดึงข้อมูล User (สมมติว่ามีความสัมพันธ์กับ Quotation หรือ DepositSlip)
    user = _quotation.user  # หรือ depositslip.user หากสัมพันธ์กับ DepositSlip
    
    context = {
        "quotation": _quotation,
        "depositslip": _depositslip,
        "deposit_orders": _deposit_orders,
        "user": user,
    }
    
    return render(request, 'deposit_slip.html', context)
