from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import ImgForm
import openai
import environ
import os
import requests
from PIL import Image

env = environ.Env()
environ.Env.read_env()

openai.api_key = env("OPENAI_KEY")
class maskrView(View):
    def __init__(self, *args, **kwargs):
        super(maskrView, self).__init__(*args, **kwargs)

    def get(self, request):
        return render(request, 'maskrView.html')

    def post(self, request):
        resp = None
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            render(request, 'maskrView.html', {'form': form, 'loading': True})
            prompt_t = request.POST.get('prompt')
            image_t = request.POST.get('image')
            form.save()
            image_obj = form.instance
            img_resized = Image.open(image_obj.image.path)
            img_resized = img_resized.resize((512, 512))
            img_resized = img_resized.convert('RGBA')
            img_resized.save("demo.png", "")
            prompt_temp = prompt_t.replace(' ', '')
            if prompt_temp.isalpha():
                print("edit")
                resp = openai.Image.create_edit( 
                    image=open("demo.png", "rb"), 
                    prompt=prompt_t, 
                    n=1, 
                    size="512x512"
                )
                image_url = resp['data'][0]['url']
                return render(request, 'maskrView.html', {'form': form, 'uploaded': image_obj.image.url, 'processed': image_url})
            else:
                print("variation")
                resp = openai.Image.create_variation(
                    image=open("demo.png", "rb"),  
                    n=1,
                    size="512x512"
                )
                image_url = resp['data'][0]['url']
            return render(request, 'maskrView.html', {'form': form, 'uploaded': image_obj.image.url, 'processed': image_url})
        else:
            form = ImgForm()
            prompt_t = request.POST.get('prompt')
            prompt_temp = prompt_t.replace(' ', '')
            if not prompt_temp.isalpha():
                return render(request, 'maskrView.html')
            render(request, 'maskrView.html', {'form': form, 'loading': True})
            resp = openai.Image.create(
                        prompt=prompt_t,
                        n=1,
                        size="512x512"
                )
            image_url = resp['data'][0]['url']
            return render(request, 'maskrView.html', {'form': form, 'processed': image_url})

        return redirect(reverse(''))