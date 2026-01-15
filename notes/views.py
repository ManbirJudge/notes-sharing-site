from datetime import date

from django.contrib.auth import authenticate as dj_auth, logout as dj_logout, login as dj_login
from django.http import JsonResponse
from django.shortcuts import render, redirect

from notes.models import *


# general views
def index(request):
    is_authenticated = False
    is_staff = False
    user = None

    if request.user.is_authenticated:
        is_authenticated = True
        user = User.objects.get(id=request.user.id)
    if request.user.is_staff:
        is_staff = True

    return render(request, 'index.html', {
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'user': user,
        'menu': 'default'
    })


def about(request):
    is_authenticated = False
    is_staff = False
    user = None

    if request.user.is_authenticated:
        is_authenticated = True
        user = User.objects.get(id=request.user.id)
    if request.user.is_staff:
        is_staff = True

    return render(request, 'about.html', {
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'user': user,
        'menu': 'default'
    })


def contact(request):
    is_authenticated = False
    is_staff = False
    user = None

    if request.user.is_authenticated:
        is_authenticated = True
        user = User.objects.get(id=request.user.id)
    if request.user.is_staff:
        is_staff = True

    return render(request, 'contact.html', {
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'user': user,
        'menu': 'default'
    })


def login(request):
    is_authenticated = False
    is_staff = False
    user = None
    err = False

    if request.user.is_authenticated:
        is_authenticated = True
        user = User.objects.get(id=request.user.id)
    if request.user.is_staff:
        is_staff = True

    if request.method == 'POST':
        username = request.POST['emailAddress']
        password = request.POST['password']

        user = dj_auth(username=username, password=password)

        if user:
            try:
                dj_login(request, user)
                return redirect('home')
            except:
                err = True
        else:
            err = True

    return render(request, 'login.html', {
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'user': user,
        'error': err,
        'menu': 'default'
    })


def signup(request):
    is_authenticated = False
    is_staff = False
    user = None
    err = False

    if request.user.is_authenticated:
        is_authenticated = True
        user = User.objects.get(id=request.user.id)
    if request.user.is_staff:
        is_staff = True

    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        contact_no = request.POST['contactNo']
        email_address = request.POST['emailAddress']
        password = request.POST['password']
        branch = request.POST['branch']
        role = request.POST['role']

        try:
            user = User.objects.create_user(
                username=email_address,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email_address
            )
            UserData.objects.create(user=user, contact=contact_no, branch=branch, role=role)

            return redirect('login')
        except Exception as e:
            err = True
            print(f'Error while creating account: {e}')

    return render(request, 'signup.html', {
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'user': user,
        'error': err,
        'menu': 'default'
    })


# user views
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)
    err = False

    if request.method == 'POST':
        # TODO: verify: old_pwd = request.POST['old_password']
        new_pwd = request.POST['new_password']
        confirm_pwd = request.POST['confirm_password']

        if new_pwd == confirm_pwd:
            user = User.objects.get(username__exact=request.user.username)
            user.set_password(new_pwd)
            user.save()

            return redirect('profile')
        else:
            err = True

    return render(request, 'change_password.html', {
        'is_authenticated': True,
        'is_staff': user.is_staff,
        'user': user,
        'user_data': user_data,
        'error': err,
        'menu': 'default'
    })


def logout(request):
    if request.user.is_authenticated:
        dj_logout(request)
    return redirect('home')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)

    return render(request, 'profile.html', {
        'is_authenticated': True,
        'is_staff': user.is_staff,
        'user': user,
        'user_data': user_data,
        'menu': 'user'
    })


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)

    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        contact_no = request.POST['contactNo']
        branch = request.POST['branch']

        user.first_name = first_name
        user.last_name = last_name
        user_data.contact = contact_no
        user_data.branch = branch

        user.save()
        user_data.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'is_authenticated': True,
        'is_staff': user.is_staff,
        'user': user,
        'user_data': user_data,
        'menu': 'user'
    })


def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    err = None
    uploaded = False
    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)

    if request.method == 'POST':
        upload_date = date.today()
        branch = request.POST['branch']
        subject = request.POST['subject']
        file = request.FILES['file']
        description = request.POST['description']
        status = 'pending'

        try:
            Note.objects.create(
                user=user,
                upload_date=upload_date,
                branch=branch,
                subject=subject,
                file=file,
                description=description,
                status=status
            )
            uploaded = True
        except Exception as e:
            err = str(e)

    return render(request, 'upload_notes.html', {
        'is_authenticated': True,
        'is_staff': user.is_staff,
        'user': user,
        'user_data': user_data,
        'err': err,
        'uploaded': uploaded,
        'menu': 'user'
    })


def my_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    notes = Note.objects.filter(user=user)

    return render(request, 'my_notes.html', {
        'is_authenticated': True,
        'is_staff': user.is_staff,
        'notes': notes,
        'menu': 'user'
    })


def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    notes = Note.objects.filter(status='accepted')

    return render(request, 'all_notes.html', {
        'is_authenticated': True,
        'is_staff': request.user.is_staff,
        'menu': 'user',
        'notes': notes
    })


def api_dlt_my_note(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    note = Note.objects.get(id=pid)
    if note.user.username != request.user.username:
        return JsonResponse({
            'err': 'This note doesn\'t belong to you.'
        })

    note.delete()
    return JsonResponse({
        'err': None
    })


# admin views
def admin_login(request):
    is_authenticated = request.user.is_authenticated
    is_staff = request.user.is_staff
    err = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = dj_auth(username=username, password=password)

        if user:
            try:
                if user.is_staff:
                    dj_login(request, user)
                    return redirect('admin_home')
                else:
                    err = 'You are not an administrator.'
                    is_authenticated = True
            except Exception as e:
                err = f'Server error: {e}'
        else:
            err = 'Invalid credentials.'

    return render(request, 'admin_login.html', {
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'err': err,
        'menu': 'admin'
    })


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('admin_login')

    all_notes_count = Note.objects.all().count()
    pending_notes_count = Note.objects.filter(status='pending').count()
    rejected_notes_count = Note.objects.filter(status='rejected').count()
    accepted_notes_count = Note.objects.filter(status='accepted').count()

    data = {
        'is_authenticated': True,
        'is_staff': True,
        'menu': 'admin',
        'all_notes_count': all_notes_count,
        'pending_notes_count': pending_notes_count,
        'rejected_notes_count': rejected_notes_count,
        'accepted_notes_count': accepted_notes_count,
    }

    return render(request, 'admin_home.html', data)


def verify_notes(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    notes = Note.objects.all()

    return render(request, 'verify_notes.html', {
        'is_authenticated': True,
        'is_staff': True,
        'menu': 'admin',
        'notes': notes
    })


def api_dlt_note(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')

    note = Note.objects.get(id=pid)
    note.delete()

    return JsonResponse({
        'err': None
    })


def api_set_note_status(request, pid):
    if not request.user.is_staff:
        return redirect('admin-login')

    status = request.POST.get('status')

    note = Note.objects.get(id=pid)
    note.status = status
    note.save()

    return JsonResponse({
        'err': None
    })
