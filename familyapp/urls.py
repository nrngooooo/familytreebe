from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/<str:uid>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:uid>/delete/', DeleteUserView.as_view()),
    path('person/', PersonCreateView.as_view()),
    path('person/<str:element_id>/', PersonEditView.as_view()),
    path('relationship/', AddRelationshipView.as_view()),
]
