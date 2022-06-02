from django.views import View
from django.http import JsonResponse

from missing_trees.setup import setup_dataframe
from missing_trees.actions import find_missing_trees


class MissingTreesViewSet(View):

    def dispatch(self, request, *args, **kwargs):

        if request.method == 'GET':
            return super().dispatch(request, *args, **kwargs)
        else:
            return JsonResponse({'detail': 'Not allowed'}, status=401)

    def get(self, request, orchard_id=''):

        try:
            draw = False
            if 'draw' in request.GET:
                draw = True
        
            trees_dictionary, trees_polygon, dataframe = setup_dataframe(orchard_id, draw)

            missing_trees = find_missing_trees(trees_dictionary, trees_polygon, dataframe)

            return JsonResponse({'missing_trees': missing_trees}, status=200)

        except Exception as e:
            return JsonResponse({'detail':str(e)}, status=400)