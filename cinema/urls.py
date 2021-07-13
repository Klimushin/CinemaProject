from django.urls import path

from cinema.views import SessionListView, TomorrowSessionListView, CreateHallView, UpdateHallView, CreateSessionView, \
    UpdateSessionView, CreateTicketView

app_name = 'cinema'
urlpatterns = [
    path('', SessionListView.as_view(), name='today'),
    path('tomorrow/', TomorrowSessionListView.as_view(), name='tomorrow'),
    path('create-hall/', CreateHallView.as_view(), name='create_hall'),
    path('update-hall/<slug:slug>/', UpdateHallView.as_view(), name='update_hall'),
    path('create-session/', CreateSessionView.as_view(), name='create_session'),
    path('update-session/<int:pk>/', UpdateSessionView.as_view(), name='update_session'),
    path('create-ticket/', CreateTicketView.as_view(), name='create_ticket'),
]
