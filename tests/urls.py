from django.urls import path

from . import views

app_name = 'tests'
urlpatterns = [
    path('', views.index, name='home'),
    path('tests/start', views.start_test, name='start_test'),
    path('tests/submit', views.finish_test, name='submit_test'),
    path('tests/new', views.CreateNewSource.as_view(), name='new_test'),
    path('tests/detail/<int:pk>', views.DetailSource.as_view(), name='test_detail'),
    path('tests/<int:id>', views.attempt_detail, name='attempt'),
    path('tests/', views.attempts_list, name='attempts_list'),
    path('answer/submit', views.submit_answer, name='submit_answer'),
]
