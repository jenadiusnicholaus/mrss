from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import pandas as pd
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, View
from .models import *
from .forms import *
from django.db.models import Q
from .forms import ProblemForm


class ProblemList(ListView):
    model = Problems
    template_name = 'index.html'
    # context_object_name = ''


class PresentProblem(View):

    def get(self, *args, **kwargs):
        form = ProblemForm()
        context = {
            'form': form
        }
        return render(self.request, 'present_problem.html', context)

    def post(self, *args, **kwargs):
        form = ProblemForm(self.request.POST or None, self.request.FILES or None)

        if form.is_valid():
            print(form)
            device_type = form.cleaned_data.get('device_type')
            device_brand = form.cleaned_data.get('device_brand')
            title = form.cleaned_data.get('title')
            image = form.cleaned_data.get('image')
            problem_desc = form.cleaned_data.get('problem_desc')
            problem = Problems()
            problem.user = self.request.user.userprofile
            problem.title =title
            problem.image=image
            problem.device_brand =device_brand
            problem.device_type =device_type
            problem.problem_desc = problem_desc
            problem.slug = slugify(title)
            problem.save()
            messages.success(self.request, 'Thanks for presenting your problem to MRSS')
            return redirect('/')
        else:
            print('form not valid')
            messages.warning(self.request, 'Your form was not valid try to fill all field')
            return redirect('core:presentProblem')


class problemDetails(DetailView):
    model = Problems
    template_name = 'problem_details.html'


def post_comments(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            new_comment = Comments()
            new_comment.user = request.user
            new_comment.solution_id = solution
            new_comment.content = content
            new_comment.save()

            messages.info(request, 'your messages is submitted successfully')

            return redirect('core:problem_details', slug=solution.problem_id.slug)
        else:
            messages.info(request, 'form is invalid')
            return redirect('core:problem_details', slug=solution.problem_id.slug)
    return redirect('core:problem_details', slug=solution.problem_id.slug)


def View_comments(request, pk=None):
    solution = get_object_or_404(Solution, pk=pk)
    comments_qs = Comments.objects.filter(solution_id=solution)
    context = {
        'comment': comments_qs
    }
    return render(request, 'comments.html', context)


def predict_chances(request):
    # Receive data from client
    # gre = int(request.GET['gre'])
    # toefl = int(request.GET['toefl'])
    # cgpa = float(request.GET['cgpa'])
    if request.method == "POST":
        gre = int(request.POST['gre_score'])
        toefl = int(request.POST['toefl_score'])
        cgpa = float(request.POST['cgpa'])

        model = pd.read_pickle(r"/home/jena/PycharmProjects/mrss/core/lr_model.pickle")
        chances = model.predict([[gre, toefl, cgpa]])
        return HttpResponse(f"{chances[0] * 100:.2f}%")


# Todo  add models data to tempalate

def blog_post_view(request):
    blog_post_qs = BlogPost.objects.all()
    context = {
        'post_list': blog_post_qs,
    }
    return render(request, 'blog.html', context)


def search_problem(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        problem_submitted = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(problem_type__icontains=query)

            results = Problems.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': problem_submitted}

            return render(request, 'index.html', context)

        else:
            return render(request, 'index.html')

    else:
        return render(request, 'index.html')
