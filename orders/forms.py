from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(max_value=9, min_value=1)


class CouponApplyForm(forms.Form):
    code = forms.CharField(max_length=30)
