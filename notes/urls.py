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

    path('change-password', change_password, name='change_password'),
    path('logout', logout, name='logout'),
    path('profile', profile, name='profile'),
    path('edit-profile', edit_profile, name='edit_profile'),
    path('upload-notes', upload_notes, name='upload_notes'),
    path('my-notes', my_notes, name='my_notes'),
    path('all-notes', all_notes, name='all_notes'),
    path('api/delete-my-note/<int:pid>/', api_dlt_my_note, name='api_dlt_my_note'),

    path('admin-home', admin_home, name='admin_home'),
    path('verify-notes', verify_notes, name='verify_notes'),
    path('api/delete-note/<int:pid>/', api_dlt_note, name='api_dlt_note'),
    path('api/set-note-status/<int:pid>/', api_set_note_status, name='api_set_note_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
