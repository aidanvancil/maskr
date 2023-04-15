from django.shortcuts import render, redirect, reverse
from maskr_app.models import Images
from django.http import HttpResponse
from django.views.generic import View

class maskrView(View):
    def __init__(self, *args, **kwargs):
        super(maskrView, self).__init__(*args, **kwargs)

    def get(self, request):
        return render(request, 'maskrView.html')

    def post(self, request):            
        return redirect(reverse(''))