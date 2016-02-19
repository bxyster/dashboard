# -*- coding: utf-8 -*-
import sys
import os
import pexpect
import datetime

from gitdashboard.models import Branch, Repo
from gitdashboard import settings

from django.http import HttpResponseRedirect

def run_as_xybian(command):
  # Now login as xybian to run command
  print 'su xybian -c "{0}"'.format(command)

  process = pexpect.spawn('su xybian -c "{0}"'.format(command))
  process.logfile = open('/tmp/log_', 'wa')
 
  return process 

def list_submit(confs):
  repo = str(confs.get('rname', None))
  branch_id = str(confs.get('branch', None))
  branch = str(Branch.objects.get(id=branch_id))

  name = repo.replace('/','__')+"-"+branch+".html"
  templatedir = settings.TEMPLATE_DIR.format(name)
  
  path = settings.REPO_DIR.format(repo)

  if os.path.exists(path):

    os.chdir(path)
    #process = run_as_xybian('cd {0}'.format(path))
    #process.expect(pexpect.EOF)  
  
    process = run_as_xybian('git --git-dir={0}/.git fetch origin'.format(path))
    process.expect(pexpect.EOF)

    process = run_as_xybian('git --git-dir={0}/.git reset --hard origin/{1}'.format(path, branch))
    process.expect(pexpect.EOF)

    process = run_as_xybian('git --git-dir={0}/.git checkout {1}'.format(path, branch))
    process.expect(pexpect.EOF)

    process = run_as_xybian('/tools/repository/gitinspector/gitinspector/gitinspector.py -f xml --format=html --timeline --localize-output -w > {0}'.format(templatedir))
    process.expect(pexpect.EOF)
  
  else:
    process = run_as_xybian('git clone --reference /data/gitcaches gitosis@10.0.0.160:{0} {1}'.format(branch, path))
    process.expect(pexpect.EOF)

    #process = run_as_xybian('cd {0}'.format(path))
    #process.expect(pexpect.EOF)
    os.chdir(path)

    #process.expect(pexpect.EOF)
  
    process = run_as_xybian('git --git-dir={0}/.git checkout {1}'.format(path, branch))
    process.expect(pexpect.EOF)

    process = run_as_xybian('/tools/repository/gitinspector/gitinspector/gitinspector.py -f xml --format=html --timeline --localize-output -w > {0}'.format(templatedir))
    process.expect(pexpect.EOF)
    
  #return HttpResponseRedirect('details/{0}/{1}/'.format(repo, branch))
  return True
  

def generate_html(repo, branch):
  name = repo.replace('/','__')+"-"+branch+".html"
  if os.path.exists('/data/allrepo/'+repo):
    os.chdir('/data/allrepo/'+repo)
    os.system('git fetch origin')
    os.system('git reset --hard origin/'+branch)
    os.system('git checkout '+branch)

    os.system('/tools/repository/gitinspector/gitinspector/gitinspector.py -f xml --format=html --timeline --localize-output -w > /root/django_dashboard/dashboard_git/dashboard/gitdashboard/templates/gitdashboard/'+name)
  else:
    os.system('git clone --reference /data/gitcaches gitosis@10.0.0.160:'+repo+' /data/allrepo/'+repo)
    os.chdir('/data/allrepo/'+repo)
    os.system('git checkout '+branch)

    os.system('/tools/repository/gitinspector/gitinspector/gitinspector.py -f xml --format=html --timeline --localize-output -w > /root/django_dashboard/dashboard_git/dashboard/gitdashboard/templates/gitdashboard/'+name)
