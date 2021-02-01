from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('explanation/', views.explanation, name='explanation'),
	path('generator/', views.generator, name='generator'),
	path('validator/', views.validator, name='validator'),

	path('generator_results/', views.generate_cpf, name="generate_cpf"),
	path('validator_results/', views.validate_cpf, name="validate_cpf"),
]