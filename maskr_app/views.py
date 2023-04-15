from django.shortcuts import render, redirect, reverse
from maskr_app.models import Images
from django.http import HttpResponse
from django.views.generic import View
from .forms import ImgForm
import numpy as np
import cv2

IMG_DIM = (512, 512)
class maskrView(View):
    def __init__(self, *args, **kwargs):
        super(maskrView, self).__init__(*args, **kwargs)

    def get(self, request):
        return render(request, 'maskrView.html')

    def post(self, request):
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image = form.instance
            return render(request, 'maskrView.html', {'form': form, 'uploaded': image})
        else:
            form = ImgForm()
        

        return redirect(reverse(''))