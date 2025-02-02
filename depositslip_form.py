from datetime import datetime
from django.shortcuts import render, redirect
from pApp.models import depositslip, deposit_orders, quotation


def depositslip_form(request, quotation_number):

    if request.method == 'POST':
        # ดึงค่าจากฟอร์ม
        current_date = datetime.now()
        date_str = current_date.strftime("%Y%m%d")
        depositslip_number = date_str + str(depositslip.objects.count() + 1)

        related_quotation = quotation.objects.get(number=quotation_number)
        # สร้าง depositslip ใหม่และบันทึกลงฐานข้อมูล
        depositslip.objects.create(
            quotation = related_quotation,
            depositslip_number=depositslip_number,
            depositslip_date=current_date,
            deposit_total=0,
            deposit_vat=0,
            deposit_totalprice=0,
            deposit_totalpriceTH="test",
            deposit_status="test",
        )

        deposit_ordername = request.POST.get('deposit_ordername', '').strip()
        deposit_prices = request.POST.get('deposit_price', '').strip()

        related_deposit = depositslip.objects.get(depositslip_number=depositslip_number)
        _deposit_total = 0

        # สร้าง deposit_orders ใหม่ที่เชื่อมโยงกับ depositslip
        for i in range(len(deposit_ordername)):
            deposit_price = int(deposit_prices[i]) if deposit_prices[i].isdigit() else 0

            _deposit_total += deposit_price
            _deposit_vat = _deposit_total * 0.07 #ภาษี
            _deposit_totalprice = _deposit_total * 1.07 

            deposit_orders.objects.create(

                depositslip = related_deposit,
                deposit_ordername=deposit_ordername[i].strip(),
                deposit_price=deposit_price,
            )


        related_deposit.deposit_vat = _deposit_vat
        related_deposit.deposit_total = _deposit_total
        related_deposit.deposit_totalprice = _deposit_totalprice
        # ดึงรายการสั่งซื้อจากฟอร์ม
        return redirect('/depositslipmanage/{}'.format(quotation_number))  # เปลี่ยนเส้นทางเมื่อบันทึกสำเร็จ

    return render(request, 'depositslip_form.html', {'quotation_number': quotation_number})
