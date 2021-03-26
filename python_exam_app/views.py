from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Job, Category
import bcrypt

def root(request):
    return render(request,'welcome.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed
    )
    request.session['user_id'] = new_user.id
    return redirect('/dashboard')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    this_user = User.objects.filter(email = request.POST['email'])
    request.session['user_id'] = this_user[0].id
    return redirect('/dashboard')

def main(request):
    if 'user_id' not in request.session:
        messages.error(request,"Please log on.")
        return redirect('/')
    context = {
        'user' : User.objects.get(id=int(request.session['user_id'])),
        'jobs': Job.objects.all(),
    }
    return render(request,'dashboard.html',context)

def logout(request):
    request.session.clear()
    return redirect('/')

def newjob(request):
    context = {
        'user' : User.objects.get(id=int(request.session['user_id']))
    }
    return render(request,'newjob.html',context)

def addjob(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/newjob')
    new_job = Job.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        location = request.POST['location'],
        created_by = User.objects.get(id=request.session['user_id']),
    )
    if len(request.POST['other']) >1:
        category = Category.objects.create(
            cat_name = request.POST['other']
        )
        new_job.categories.add(category)
    
    if  'lawncare' not in request.POST:
        checked = True
    else:
        lawncare = Category.objects.get(id=1)
        new_job.categories.add(lawncare)
    if 'housekeeping' not in request.POST:
        checked = True
    else:
        house = Category.objects.get(id=2)
        new_job.categories.add(house)
    if 'pet_watching' not in request.POST:
        checked = True
    else:
        pet = Category.objects.get(id=3)
        new_job.categories.add(pet)
    return redirect('/dashboard')

def viewjob(request, job_id):
    
    context = {
        'job' : Job.objects.get(id=job_id),
        'user' : User.objects.get(id=int(request.session['user_id']))
    }
    return render(request,'viewjob.html',context)

def destroy(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect('/dashboard')

def edit(request, job_id):
    context = {
        'job' : Job.objects.get(id= job_id),
        'user' : User.objects.get(id=int(request.session['user_id'])),
    }
    return render(request,'editjob.html',context)

def makechange(request, job_id):
    errors = Job.objects.job_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/jobs/edit/{job_id}')
    job = Job.objects.get(id=job_id)
    job.title = request.POST['title']
    job.desc = request.POST['desc']
    job.location = request.POST['location']
    job.save()
    return redirect('/dashboard')

def assign(request, job_id):
    job = Job.objects.get(id=job_id)
    user = User.objects.get(id=int(request.session['user_id']))
    job.performed_by.add(user)
    return redirect('/dashboard')
def quit (request, job_id):
    job = Job.objects.get(id=job_id)
    user = User.objects.get(id=int(request.session['user_id']))
    job.performed_by.remove(user)
    return redirect('/dashboard')