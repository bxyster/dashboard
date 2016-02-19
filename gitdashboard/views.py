from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils import timezone
from .models import Repo, Branch
from collections import defaultdict
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from gitdashboard import settings
from gitdashboard.forms import AddListForm, SubmitListForm
from django.db import IntegrityError
from gitdashboard import utils
from django.http import HttpResponseRedirect

# Create your views here.
def check_user_allowed(user):
  """
  test for user_passes_test decorator
  """
  if settings.STAFF_ONLY:
    return user.is_authenticated() and user.is_staff
  else:
    return user.is_authenticated()

@user_passes_test(check_user_allowed)
def list_lists(request):
  """
  Homepage view - list of lists a user can view, and can add
  """
  # Make sure user belongs to at least one group.
  group_count = request.user.groups.all().count()
  if group_count == 0:
    messages.error(request, "You do not yet belong to any groups. Ask your administrator to add you to one.")
  
  # Only show lists to the user that belong to groups they are members of.
  # Superusers see all lists
  if request.user.is_superuser:
    list_list = Repo.objects.all().order_by('group', 'rname')
  else: 
    list_list = Repo.objects.filter(group__in=request.user.groups.all).order_by('group', 'rname')
  
  # Count everything
  list_count = list_list.count()

  date = datetime.date.today()

  return render_to_response('gitdashboard/list_lists.html', locals(), context_instance=RequestContext(request))
  
@user_passes_test(check_user_allowed)
def add_list(request):
  """
  Allow users to add a new repo list to the group they're in.
  """
  if request.POST:
    form = AddListForm(request.user, request.POST)
    if form.is_valid():
      try:
        form.save()
        messages.success(request, "A new list has been added.")
        return HttpResponseRedirect(request.path)
      except IntegrityError:
        messages.error(request,
                      "There was a problem saving the new list. "
                      "Most likely a list with the same name in the same group already exists.")
  else:
    if request.user.groups.all().count() == 1:
      form = AddListForm(request.user, initial = {"group": request.user.groups.all()[0]})
    else:
      form = AddListForm(request.user)
  return render_to_response('gitdashboard/add_list.html', locals(), context_instance=RequestContext(request))

def repo_list(request):
  repos = Repo.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
  res = defaultdict(list)
  des = [ (repo.rname, repo.branch) for repo in repos ]
  for k, v in des:
    res[k.replace('/','__')].append(v)
  date = datetime.date.today()
  return render(request, 'gitdashboard/repo_list.html', {'res': res.items(), 'date': date})

def repo_detail(request, repo, branch, day):
  request.GET.get('repo')
  request.GET.get('branch')
  request.GET.get('day')
  return render(request, "gitdashboard/"+repo+"-"+branch+"-"+day+".html")

def details(request, repo, branch):
  request.GET.get('repo')
  request.GET.get('branch')
 
  name = repo.replace('/','__')+"-"+branch+".html" 
  return render(request, "gitdashboard/"+name)

@user_passes_test(check_user_allowed)
def list_submit(request):
  if request.POST:
    form = SubmitListForm(request.user.groups.all(), request.POST)
    if form.is_valid():
      data = form.clean()
      repo = str(data['rname'])
      branch_id = str(data['branch'])
      branch = str(Branch.objects.get(id=branch_id))
      messages.success(request, "Repo:"+repo+", Branch:"+branch)
      utils.list_submit(form.clean())
      #return HttpResponseRedirect("gitdashboard/"+repo+"-"+branch+".html")
      #return HttpResponseRedirect('/list_repo/')
      #return HttpResponseRedirect("gitdashboard/"+repo+"-"+branch+".html")
      #return HttpResponseRedirect('details/{0}/{1}/'.format(repo, branch))
      name = repo.replace('/','__')+"-"+branch+".html"
      return render(request, "gitdashboard/"+name)

       
  else:
      form = SubmitListForm(request.user.groups.all())

  return render_to_response('gitdashboard/list_submit.html', {'form': form}, context_instance=RequestContext(request))
  #return HttpResponseRedirect("gitdashboard/"+repo+"-"+branch+".html")

@user_passes_test(check_user_allowed)
def list_repo(request):
  repos = Repo.objects.all()
  return render_to_response('gitdashboard/list_repo.html', {'repos': repos})
