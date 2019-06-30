from django.urls import path
from .views import (
    IndexView, SummaryView, LoginView, AuthenticationView, ProfileView, SavedView,
    LookupView, GeolocationAutocompleteView, DetailAutocompleteView
)

urlpatterns = [
    path('', IndexView.as_view()),
    path('summary/', SummaryView.as_view()),
    path('login/', LoginView.as_view()),
    path('auth/', AuthenticationView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('saved/', SavedView.as_view()),
    path('saved/<str:kind>/<int:pk>/', SavedView.as_view()),
    path('geolocation-autocomplete/', GeolocationAutocompleteView.as_view()),
    path('detail-autocomplete/', DetailAutocompleteView.as_view()),
    path('lookup/<str:kind>/', LookupView.as_view())
]
