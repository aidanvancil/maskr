from django.shortcuts import render, redirect, reverse
from maskr_app.models import Images
from django.http import HttpResponse
from django.views.generic import View
from django.core.files import File
from .forms import ImgForm
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import numpy as np
import cv2
import matplotlib.pyplot as plt


checkpoint = "model.pth"
model_type = "vit_h"

sam = sam_model_registry[model_type](checkpoint=checkpoint)
mask_generator = SamAutomaticMaskGenerator(sam)

class maskrView(View):
    def __init__(self, *args, **kwargs):
        super(maskrView, self).__init__(*args, **kwargs)

    def get(self, request):
        return render(request, 'maskrView.html')

    def post(self, request):
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_obj = form.instance
            image = cv2.imread(image_obj.image.path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            masks = mask_generator.generate(image)
            
            plt.figure(figsize=(20,20))
            plt.imshow(image)
            #self.show_anns(masks)
            plt.axis('off')
            plt.savefig('placeholder.png')
            with open('placeholder.png', 'rb') as f:
                print(dir(File(f)))
                return render(request, 'maskrView.html', {'form': form, 'uploaded': image_obj, 'processed': File(f)})
            return render(request, 'maskrView.html', {'form': form, 'uploaded': image_obj})
        else:
            form = ImgForm()
        return redirect(reverse(''))
    
    def show_anns(self, anns):
        if len(anns) == 0:
            return
        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
        ax = plt.gca()
        ax.set_autoscale_on(False)
        polygons = []
        color = []
        for ann in sorted_anns:
            m = ann['segmentation']
            img = np.ones((m.shape[0], m.shape[1], 3))
            color_mask = np.random.random((1, 3)).tolist()[0]
            for i in range(3):
                img[:,:,i] = color_mask[i]
            ax.imshow(np.dstack((img, m*0.35)))
        return 