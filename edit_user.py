import base64
from django.core.files.base import ContentFile
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from pApp.models import user

def edit_user(request, user_id):
    _user = get_object_or_404(user, id=user_id)

    if request.method == "POST":
        # อัปเดตข้อมูลผู้ใช้
        _user.name = request.POST.get('name')
        _user.lastName = request.POST.get('lastName')
        _user.email = request.POST.get('email')
        _user.tel = request.POST.get('tel')
        _user.address = request.POST.get('address')

        # บันทึกลายเซ็น
        signature_data = request.POST.get('signature')
        if signature_data:
            format, imgstr = signature_data.split(';base64,')
            img_data = base64.b64decode(imgstr)

            # ระบุเส้นทางสำหรับบันทึกไฟล์ลายเซ็น
            signature_path = os.path.join(settings.BASE_DIR, 'static', 'signature.png')

            # บันทึกไฟล์ลายเซ็น
            with open(signature_path, 'wb') as f:
                f.write(img_data)

        _user.save()
        messages.success(request, "ข้อมูลผู้ใช้และลายเซ็นถูกอัปเดตเรียบร้อยแล้ว!")
        return redirect('/showProfile')  # เปลี่ยน URL เป็นเส้นทางที่เหมาะสม

    context = {
        'user': _user,
    }
    return render(request, 'edit_user.html', context)
