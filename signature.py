from django.shortcuts import render, redirect
from django.http import HttpResponse
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings

def signature_view(request):
    # รับค่า quotation_number จาก URL
    quotation_number = request.GET.get('quotation_number')

    # ตรวจสอบว่า quotation_number ถูกส่งมาหรือไม่
    if not quotation_number:
        return HttpResponse("Quotation number is missing!")

    if request.method == "POST":
        signature_data = request.POST.get('signature_data')
        
        if signature_data and quotation_number:
            try:
                # ลบ prefix 'data:image/png;base64,' ออก
                if signature_data.startswith('data:image/png;base64,'):
                    signature_data = signature_data.split(',')[1]
                else:
                    return HttpResponse("Invalid signature data format!")

                # แปลงจาก base64 เป็น Image
                img_data = base64.b64decode(signature_data)
                image = Image.open(BytesIO(img_data))

                # ตั้งชื่อไฟล์ตาม quotation.number
                filename = f"{quotation_number}.png"
                save_path = os.path.join(settings.BASE_DIR, 'pApp', 'static', 'signatures', filename)

                # สร้างโฟลเดอร์ static/signatures หากยังไม่มี
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # บันทึกภาพลงใน static/signatures/
                image.save(save_path)

                # Redirect กลับไปที่หน้ารายละเอียดของ quotation โดยใช้ quotation_number
                return redirect(f'/quotation/{quotation_number}/')

            except Exception as e:
                return HttpResponse(f"Error saving signature: {str(e)}")
        else:
            return HttpResponse("Missing signature data or quotation number!")

    return render(request, "signature.html", {'quotation_number': quotation_number}) 
