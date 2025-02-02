from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from pApp.models import quotation, order

def form(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        lastname = request.POST.get('lastName', '').strip()
        address = request.POST.get('address', '').strip()
        tel = request.POST.get('tel', '').strip()

        if not name or not lastname or not address or not tel:
            return render(request, "form.html", {"error": "กรุณากรอกข้อมูลให้ครบถ้วน"})

        # สร้างหมายเลข Quotation
        current_date = datetime.now()
        date_str = current_date.strftime("%Y%m%d")
        quotation_number = date_str + str(quotation.objects.count() + 1)

        # สร้าง Quotation
        new_quotation = quotation.objects.create(
            date=current_date,
            number=quotation_number,
            name=name,
            lastName=lastname,
            address=address,
            tel=tel,

            totalPrice = 0
        )

        quotation_url = reverse('quotation', kwargs={'quotation_number': quotation_number})
        quotation_view_url = reverse('quotation_view', kwargs={'quotation_number': quotation_number})

        # สมมุติว่า new_quotation คือออบเจ็กต์ของ Quotation ที่จะอัปเดต
        new_quotation.url = quotation_url  # อัปเดต URL ของ Quotation
        new_quotation.quotation_view_url = quotation_view_url  # อัปเดต URL สำหรับ quotation_view
        new_quotation.save()  # บันทึกการเปลี่ยนแปลง
        # สร้าง Orders
        create_orders(request, quotation_number)

        # ส่ง URL ไปแสดงใน Popup
        return render(request, "form.html", {"success": True, "quotation_view_url": quotation_view_url})

    return render(request, "form.html")


def create_orders(request, quotation_number):
    # รับข้อมูลจากฟอร์ม
    order_names = request.POST.getlist('order_names', [])
    amounts = request.POST.getlist('amounts', [])
    prices = request.POST.getlist('prices', [])

    try:
        # ค้นหา Quotation
        related_quotation = quotation.objects.get(number=quotation_number)
        
        total_price_sum = 0  # สำหรับคำนวณผลรวมของ total

        # สร้าง Orders
        for i in range(len(order_names)):
            amount = int(amounts[i]) if amounts[i].isdigit() else 0
            price = int(prices[i]) if prices[i].isdigit() else 0
            total = amount * price
            total_price_sum += total  # เพิ่มค่า total ของแต่ละ order ลงใน total_price_sum

            # สร้าง Order แต่ไม่รวม totalPrice ยัง
            order.objects.create(
                quotation=related_quotation,
                orderName=order_names[i].strip(),
                amount=amount,
                price=price,
                total=total,
            )

        # อัปเดต totalPrice ของ Quotation หลังจากสร้าง Orders ทั้งหมด
        related_quotation.totalPrice = total_price_sum
        related_quotation.save()  # บันทึกการเปลี่ยนแปลงของ quotation


        return redirect("/adminmanage/manage")  # เปลี่ยนไปหน้าคำสั่งซื้อสำเร็จ
    except quotation.DoesNotExist:
        return render(request, "form.html")


