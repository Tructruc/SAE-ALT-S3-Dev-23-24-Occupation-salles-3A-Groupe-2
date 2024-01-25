from random import shuffle
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Sensor
from django.db.models import Q
import re

class AutoCompletSearchViewSet(APIView):
    @staticmethod
    def natural_sort_key(s):
        """
        Une fonction auxiliaire pour obtenir une clé de tri naturel.
        """
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


    def get(self, request, format=None):
        query = request.GET.get('q', '')
        suggestions_set = set()  # Utiliser un ensemble pour éviter les doublons

        if query:
            sensors = Sensor.objects.all()[:100]  # Limitez le nombre de sensors si nécessaire

            for sensor in sensors:
                # Vérifier chaque champ pour une correspondance exacte avec la requête
                if query in sensor.room:
                    suggestions_set.add(sensor.room)
                if query in sensor.devicename:
                    suggestions_set.add(sensor.devicename)
                if query in sensor.deveui:
                    suggestions_set.add(sensor.deveui)
                # Ajoutez ici d'autres champs si nécessaire

        # Convertir l'ensemble en liste pour la réponse
        suggestions = list(suggestions_set)
        # Trier la liste de suggestions
        suggestions = sorted(suggestions_set, key=AutoCompletSearchViewSet.natural_sort_key)


        return Response(suggestions)
