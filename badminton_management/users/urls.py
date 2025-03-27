from django.urls import path
from .views import register, user_login, user_logout
from .views import admin_dashboard, player_dashboard, dashboard
from .views import add_court, book_court, view_bookings, manage_bookings


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('player-dashboard/', player_dashboard, name='player_dashboard'),

      # Court Management
    path('add-court/', add_court, name='add_court'),
    path('book-court/', book_court, name='book_court'),
    path('view-bookings/', view_bookings, name='view_bookings'),
    path('manage-bookings/', manage_bookings, name='manage_bookings'),
    
]
