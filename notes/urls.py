from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from notes.views import *

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('admin-login', admin_login, name='admin_login'),
    path('admin-home', admin_home, name='admin_home'),
    path('logout', logout, name='logout'),
    path('profile', profile, name='profile'),
    path('change-password', change_password, name='change_password'),
    path('edit-profile', edit_profile, name='edit_profile'),
    path('upload-notes', upload_notes, name='upload_notes'),
    path('view-my-notes', view_my_notes, name='view_my_notes'),
    path('view-all-notes', view_all_notes, name='view_all_notes'),
    path('delete-my-note(?<int:pid>)', delete_my_note, name='delete_my_note'),
    path('delete-note(?<int:pid>)', delete_note, name='delete_note'),
    path('view-users', view_users, name='view_users'),
    path('delete-user(?<int:pid>)', delete_user, name='delete_user'),
    path('view-notes', view_notes, name='view_notes'),
    path('view-pending-notes', view_pending_notes, name='view_pending_notes'),
    path('view-accepted-notes', view_accepted_notes, name='view_accepted_notes'),
    path('view-rejected-notes', view_rejected_notes, name='view_rejected_notes'),
    path('assign-note-status(?<status>,<int:pid>,<redirect_to>)', assign_note_status, name='assign_note_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
