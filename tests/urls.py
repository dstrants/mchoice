from django.urls import path

from . import views

app_name = 'tests'
urlpatterns = [
    path('', views.index, name='home'),
    path('import/start', views.start_import, name='start_import'),
    path('import/process', views.import_tests, name='import'),
    path('test/start', views.start_test, name='start_test'),
    path('test/submit', views.finish_test, name='submit_test'),
    path('answer/submit', views.submit_answer, name='submit_answer'),

]