from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from gitdashboard.models import Repo, Branch
import re
from collections import defaultdict
from django.db.models import Count

class AddListForm(ModelForm):
  # The picklist showing allowable groups to which a new list can be added
  # determines which groups the user belongs to. This queries the form object
  # to derive that list.
  def __init__(self, user, *args, **kwargs):
    super(AddListForm, self).__init__(*args, **kwargs)
    self.fields['group'].get_queryset = Group.objects.filter(user=user)

  class Meta:
    model = Repo

class ListForm(forms.CharField):
  def validate(self, value):
    super(ListForm, self).validate(value)
  
    if len(re.sub('[a-z_\.-]', '', value)) > 0:
      raise forms.ValidationError('Not right')

class SubmitListForm(forms.Form):
  #name = ListForm(max_length=50, label=u'name')
  #name = forms.CharField(label='name', max_length=100)
  def __init__(self, groups, *args, **kwargs):
    super(SubmitListForm, self).__init__(*args, **kwargs)
    #self.fields['rname'].choices =(('a', 'b'), ('c', 'd'))
    #self.fields['rname'].help_text = "Repository Name"
    q1 = Repo.objects.filter(group__in=groups).values_list('rname',flat=True).annotate(count=Count('rname'))
    data = [(str(o), str(o)) for o in q1]
    self.fields['rname'] = forms.ChoiceField(choices=data)
    self.fields['branch'] = forms.ChoiceField(choices=[(o.id, o.branch) for o in Repo.objects.all()])
    #repo = self.cleaned_data.get('rname')
    #self.fields['branch'] = forms.ChoiceField(choices=[(str(o), str(o)) for o in Repo.objects.filter(rname=repo)])
  class Meta:
    model = Repo
    #exclude = ('created_date', 'group',)
    fields = ('rname','branch',)
  #repos = Repo.objects.all()
  #r = [repo.rname for repo in repos]
  #s = ((repo.rname,repo.branch) for repo in repos)
  #name = forms.ChoiceField(choices=r, label=u'Repository', required=True)
  #branch = forms.ChoiceField(choices=s, required=True)
  def clean(self):
    cleaned_data = super(SubmitListForm, self).clean()
    rname = str(cleaned_data.get('rname')) 
    branch = str(cleaned_data.get('branch'))
    #branch_name = str(Branch.objects.get(id=branch))
    if branch not in [str(o.branch_id) for o in Repo.objects.filter(rname=rname)]:
      #msg = "Please choose Branch correctly."
      msg = "rname:"+rname+" branch:"+branch
      self.add_error('branch', msg)
    return self.cleaned_data
