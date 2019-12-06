from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,Http404,HttpRequest
from .models import *
from django.views.generic import CreateView
from django.utils.text import slugify

# Create your views here.
def project_list(request):
    return render(request,'project-list.html')

def project_detail(request,project_slug):
    # Fetch one budget
    project = get_object_or_404(Project, slug=project_slug)
    category_list = Category.objects.filter(project=project)

    return render(request,'project-detail.html',{'project': project, 'expense_list':project.expenses.all()})


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'add-project.html'
    fields = ('name', 'budget')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project=Project.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])



