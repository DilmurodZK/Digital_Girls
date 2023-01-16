from django.shortcuts import render, redirect
from app.models import *


def home_view(request):
    return render(request, 'dashboard-default.html')


def slider_view(request):
    context = {
        "slider":Slider.objects.all(),
        "active_slider" : Slider.objects.filter(status=True).order_by('-id')
    }
    return render(request, 'slider.html', context)


def modal_slider(request, pk):
    slider = Slider.objects.get(id=pk)
    slider.status = False
    return redirect('activate-slider-url', slider.pk)

def activate_slider(request, pk):
    slider = Slider.objects.get(id=pk)
    active_slider = Slider.objects.filter(status=True)
    s_list = []
    for i in active_slider:
        if i.status == True:
            s_list.append(i)
    if slider.status == False:
        if len(s_list) == 4:
            s_list[3].status = False
            s_list[3].save()
            slider.status = True
            slider.save()
            s_list.append(slider)
        else:
            slider.status = True
            slider.save()
            s_list.append(slider)
    else:
        if len(s_list) < 4:
            slider.status = False
            slider.save()
    return redirect('slider-url')


def delete_slider(request, pk):
    slider = Slider.objects.get(id=pk)
    slider.delete()
    return redirect('slider-url')


def create_slider(request):
    if request.method == "POST":
        title_uz = request.POST.get('title_uz')
        title_ru = request.POST.get('title_ru')
        text_uz = request.POST.get('text_uz')
        text_ru = request.POST.get('text_ru')
        image = request.FILES.get('image')
        Slider.objects.create(
            title_uz=title_uz,
            title_ru=title_ru,
            text_uz=text_uz,
            text_ru=text_ru,
            image=image,
        )
        return redirect('slider-url')
    return redirect('slider-url')