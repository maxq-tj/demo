from django.shortcuts import render, get_object_or_404, redirect
from pApp.models import quotation, order
from .formeditorder import QuotationForm, OrderForm

def edit_quotation(request, number):
    _quotation = get_object_or_404(quotation, number=number)
    related_orders = order.objects.filter(quotation=_quotation)

    if request.method == 'POST':
        # ฟอร์มแก้ไขข้อมูล quotation
        form = QuotationForm(request.POST, instance=_quotation)
        
        order_forms = []
        # ส่งค่า prefix ให้กับแต่ละ order form เพื่อแยกข้อมูล POST
        for index, order_instance in enumerate(related_orders):
            order_form = OrderForm(request.POST, instance=order_instance, prefix=f'order_{index}')
            order_forms.append(order_form)

        if form.is_valid():
            form.save()  # บันทึกข้อมูล quotation
            
            # ตรวจสอบและบันทึกข้อมูลในแต่ละ order
            for order_form in order_forms:
                if order_form.is_valid():
                    order_form.save()  # บันทึกข้อมูล order

            return redirect("/adminmanage/manage/")  # เปลี่ยนเส้นทางไปยังหน้ารายการ

    else:
        form = QuotationForm(instance=_quotation)
        order_forms = [OrderForm(instance=order_instance, prefix=f'order_{index}') for index, order_instance in enumerate(related_orders)]

    return render(request, 'edit_quotation.html', {
        'form': form,
        'quotation': _quotation,
        'orders': related_orders,
        'order_forms': order_forms
    })
