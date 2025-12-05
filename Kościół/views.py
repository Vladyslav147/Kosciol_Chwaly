from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404 


from .models import GalleryPost, GalleryImage
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, template_name='main/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Cosciol:index')
    else:
        # Если это GET-запрос (просто зашли на страницу), создаем пустую форму
        form = UserCreateForm()
    return render(request, 'registers/register.html', {'form': form})


