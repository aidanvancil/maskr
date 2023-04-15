from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import ImgForm
import openai
import environ
import os
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
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            prompt_t = request.POST.get('prompt')
            image_t = request.POST.get('image')
            form.save()
            image_obj = form.instance
            img_resized = Image.open(image_obj.image.path)
            IMG_DIM = (256, 256)
            img_resized = img_resized.resize(IMG_DIM)
            img_resized.save("demo.png", "")
            print(image_obj.image.url)
            resp = None
            print(image_t)
            print(prompt_t)
            if prompt_t.isalpha() and not image_obj.image.url:
                resp = openai.Image.create(
                        prompt=prompt_t,
                        n=1,
                        size="256x256"
                )
                image_url = resp['data'][0]['url']
                return render(request, 'maskrView.html', {'form': form, 'processed': image_url})
            elif prompt_t and image_t:
                resp = openai.Image.create_edit( 
                    image=open("demo.png", "rb"), 
                    prompt=prompt_t, 
                    n=1, 
                    size="256x256"
                )
                image_url = resp['data'][0]['url']
                return render(request, 'maskrView.html', {'form': form, 'uploaded': image_obj.image.url, 'processed': image_url})
            else:
                """resp = openai.Image.create_variation(
                    image=open("demo.png", "rb"),
                    n=1,
                    size="256x256"
                )
                image_url = resp['data'][0]['url']"""
            return render(request, 'maskrView.html', {'form': form, 'uploaded': image_obj.image.url, 'processed': image_obj.image.url})
        else:
            form = ImgForm()
        return redirect(reverse(''))