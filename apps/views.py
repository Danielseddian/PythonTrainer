from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .forms import ResolveForm, CreationForm
from .models import Task, Solution
from .tools import make_folder_name, check_resolve

User = get_user_model()


@login_required
def index(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 1)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    try:
        resolve = Solution.objects.get(user=request.user, task=page[0])
    except ObjectDoesNotExist:
        resolve = Solution.objects.create(folder=make_folder_name(), user=request.user, task=page[0])
    form = ResolveForm(request.POST or {"resolve": resolve.resolve or page[0].default})
    resolve.resolve = form.data["resolve"]
    resolve.save()
    message = check_resolve(page[0], resolve)
    return render(request, 'index.html', {'form': form, "page": page, "message": message})


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("apps:index")
    template_name = "registration/signup.html"
