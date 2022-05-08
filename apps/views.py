from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render

from .forms import ResolveForm, CreationForm
from .models import Task
from .tools import check_resolve, get_page, get_resolve


@login_required
def index(request):
    page = get_page(Task.objects.filter(is_pub=True), request.GET.get('page'))
    resolve = get_resolve((task := page[0]), request.user)
    form = ResolveForm(request.POST or {"resolve": resolve.resolve or task.default})
    resolve.resolve = form.data["resolve"]
    resolve.save()
    return render(request, 'index.html', {'form': form, "page": page, "result": check_resolve(task, resolve)})


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("trainer:index")
    template_name = "registration/signup.html"
