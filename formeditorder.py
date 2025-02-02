from django import forms
from pApp.models import order,quotation

class QuotationForm(forms.ModelForm):
    class Meta:
        model = quotation
        fields = ['name', 'lastName', 'address']  # ฟิลด์ที่สามารถแก้ไขได้ใน order
class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['orderName', 'amount', 'price']  # ฟิลด์ที่สามารถแก้ไขได้ใน order
