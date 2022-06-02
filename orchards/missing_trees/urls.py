from django.urls import path

from missing_trees.views import MissingTreesViewSet

urlpatterns = [
    path('orchards/<int:orchard_id>/missing-trees/', MissingTreesViewSet.as_view(), name="missing-trees")
]