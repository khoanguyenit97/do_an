from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    #path('concept/<str:keyphrase>', views.concept, name='concept'),  # concept/
    #path('concept', api.find_concept, name='find_concept'),  # concept?search=
    #path('tree/<str:index_in_tree>', views.tree_item, name='tree'),  # tree/
    # path('file', views.file, name='file'),  # file/
    path('solve', api.solve, name='solve'),
]
