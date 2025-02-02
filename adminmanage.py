from django.shortcuts import render
from pApp.models import quotation

def adminmanage(request):
    # ดึงข้อมูล Quotation ทั้งหมดจากฐานข้อมูล
    quotations = quotation.objects.all()

    # ส่งข้อมูลไปยัง Template
    return render(request, 'adminmanage/index.html', {'quotations': quotations})
