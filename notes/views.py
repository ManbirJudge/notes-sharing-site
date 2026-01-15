from datetime import date

from django.shortcuts import render, redirect
# from django.utils.datetime_safe import date

from notes.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as _logout, login as _login


# Create your views here.
def index(request):
    is_authenticated = 'no'
    is_staff = 'no'

    user = None

    if request.user.is_authenticated:
        is_authenticated = 'yes'
        print("\n\n Logged In! \n\n")
        user = User.objects.get(id=request.user.id)

    if request.user.is_staff:
        is_staff = 'yes'
        print("\n\n Staff! \n\n")
        user = User.objects.get(id=request.user.id)

    data = {'is_authenticated': is_authenticated, 'is_staff': is_staff, 'user': user}

    return render(request, 'index.html', data)


def about(request):
    is_authenticated = 'no'
    is_staff = 'no'

    user = None

    if request.user.is_authenticated:
        is_authenticated = 'yes'
        print("\n\n Logged In! \n\n")
        user = User.objects.get(id=request.user.id)

    if request.user.is_staff:
        is_staff = 'yes'
        print("\n\n Staff! \n\n")
        user = User.objects.get(id=request.user.id)

    data = {'is_authenticated': is_authenticated, 'is_staff': is_staff, 'user': user}

    return render(request, 'about.html', data)


def contact(request):
    is_authenticated = 'no'
    is_staff = 'no'

    user = None

    if request.user.is_authenticated:
        is_authenticated = 'yes'
        print("\n\n Logged In! \n\n")
        user = User.objects.get(id=request.user.id)

    if request.user.is_staff:
        is_staff = 'yes'
        print("\n\n Staff! \n\n")
        user = User.objects.get(id=request.user.id)

    data = {'is_authenticated': is_authenticated, 'is_staff': is_staff, 'user': user}

    return render(request, 'contact.html', data)


def login(request):
    is_authenticated = 'no'
    is_staff = 'no'

    user = None
    error = None

    if request.user.is_authenticated:
        is_authenticated = 'yes'
        print("\n\n Logged In! \n\n")
        user = User.objects.get(id=request.user.id)

    if request.user.is_staff:
        is_staff = 'yes'
        print("\n\n Staff! \n\n")
        user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        username = request.POST['emailAddress']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        try:
            if user:
                _login(request, user)
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'

    data = {'is_authenticated': is_authenticated, 'is_staff': is_staff, 'user': user, 'error': error}

    return render(request, 'login.html', data)


def signup(request):
    error = None

    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        contact_no = request.POST['contactNo']
        email_address = request.POST['emailAddress']
        password = request.POST['password']
        branch = request.POST['branch']
        role = request.POST['role']

        try:
            user = User.objects.create_user(username=email_address, password=password, first_name=first_name,
                                            last_name=last_name, email=email_address)
            UserData.objects.create(user=user, contact=contact_no, branch=branch, role=role)

            error = 'no'
        except Exception as e:
            error = 'yes'
            print(e)

    data = {'error': error}

    return render(request, 'sign_up.html', data)


def admin_login(request):
    is_authenticated = 'no'
    is_staff = 'no'

    error = None

    if request.user.is_authenticated:
        is_authenticated = 'yes'
        print("\n\n Logged In! \n\n")

    if request.user.is_staff:
        is_staff = 'yes'
        print("\n\n Staff! \n\n")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        try:
            if user.is_staff:
                _login(request, user)
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'

    data = {'is_authenticated': is_authenticated, 'is_staff': is_staff, 'error': error}

    return render(request, 'admin_login.html', data)


def admin_home(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    all_notes_count = Note.objects.all().count()
    pending_notes_count = Note.objects.filter(status="pending").count()
    rejected_notes_count = Note.objects.filter(status="rejected").count()
    accepted_notes_count = Note.objects.filter(status="accepted").count()

    data = {
        'all_notes_count': all_notes_count,
        'pending_notes_count': pending_notes_count,
        'rejected_notes_count': rejected_notes_count,
        'accepted_notes_count': accepted_notes_count,
    }

    return render(request, 'admin_home.html', data)


def logout(request):
    _logout(request)

    return redirect('home')


def profile(request):
    # error = None

    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)

    data = {'user': user, 'user_data': user_data}

    return render(request, 'profile.html', data)


def change_password(request):
    error = None

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            user = User.objects.get(username__exact=request.user.username)

            user.set_password(new_password)
            user.save()

            error = "no"

        else:
            error = "yes"

    # user = User.objects.get(id=request.user.id)
    # user_data = UserData.objects.get(user=user)
    #
    data = {'error': error}

    return render(request, 'change_password.html', data)


def edit_profile(request):
    error = None

    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)

    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        contact_no = request.POST['contactNo']
        email_address = request.POST['emailAddress']
        branch = request.POST['branch']

        user.first_name = first_name
        user.last_name = last_name
        user_data.contact = contact_no
        user_data.branch = branch

        user.save()
        user_data.save()

        error = 'no'

    data = {'user': user, 'user_data': user_data, 'error': error}

    return render(request, 'edit_profile.html', data)


def upload_notes(request):
    error = None

    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    user_data = UserData.objects.get(user=user)

    if request.method == "POST":
        upload_date = date.today()
        branch = request.POST['branch']
        subject = request.POST['subject']
        # file = request.POST['file']
        file = request.FILES['file']
        file_type = request.POST['file_type']
        description = request.POST['description']
        status = 'pending'

        try:
            Note.objects.create(user=user, upload_date=upload_date, branch=branch, subject=subject, file=file, file_type=file_type, description=description, status=status)
            error = 'no'
        except:
            error = 'yes'

    data = {'user': user, 'user_data': user_data, 'error': error}

    return render(request, 'upload_notes.html', data)


def view_my_notes(request):
    error = None

    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(id=request.user.id)
    notes = Note.objects.filter(user=user)

    data = {'error': error, 'notes': notes}

    return render(request, 'view_my_notes.html', data)


def view_notes(request):
    error = None

    if not request.user.is_staff:
        return redirect('admin_login')

    notes = Note.objects.all()

    data = {'error': error, 'notes': notes}

    return render(request, 'view_notes.html', data)


def view_all_notes(request):
    error = None

    if not request.user.is_authenticated:
        return redirect('login')

    notes = Note.objects.filter(status='accepted')
    # notes = Note.objects.all()

    data = {'error': error, 'notes': notes}

    return render(request, 'view_all_notes.html', data)


def view_pending_notes(request):
    error = None

    if not request.user.is_staff:
        return redirect('admin_login')

    notes = Note.objects.filter(status='pending')

    data = {'error': error, 'notes': notes}

    return render(request, 'view_pending_notes.html', data)


def view_accepted_notes(request):
    error = None

    if not request.user.is_staff:
        return redirect('admin_login')

    notes = Note.objects.filter(status='accepted')

    data = {'error': error, 'notes': notes}

    return render(request, 'view_accepted_notes.html', data)


def view_rejected_notes(request):
    error = None

    if not request.user.is_staff:
        return redirect('admin_login')

    notes = Note.objects.filter(status='rejected')

    data = {'error': error, 'notes': notes}

    return render(request, 'view_rejected_notes.html', data)


def delete_my_note(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    note = Note.objects.get(id=pid)
    note.delete()

    return redirect('view_my_notes')


def delete_note(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')

    note = Note.objects.get(id=pid)
    note.delete()

    return redirect('view_notes')


def view_users(request):
    error = None

    if not request.user.is_staff:
        return redirect('admin_login')

    users = UserData.objects.all()

    data = {'error': error, 'users': users}

    return render(request, 'view_users.html', data)


def delete_user(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')

    user = User.objects.get(id=pid)
    user.delete()

    return redirect('view_users')


def assign_note_status(request, status, pid, redirect_to):
    if not request.user.is_staff:
        return redirect('admin-login')

    note = Note.objects.get(id=pid)
    note.status = status
    note.save()

    if redirect_to == 'view_pending_notes':
        return redirect('view_pending_notes')

    if redirect_to == 'view_notes':
        return redirect('view_pending_notes')

    if redirect_to == 'view_rejected_notes':
        return redirect('view_rejected_notes')

    if redirect_to == 'view_accepted_notes':
        return redirect('view_accepted_notes')
    else:
        return redirect('view_pending_notes')
