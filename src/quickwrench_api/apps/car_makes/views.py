from rest_framework.views import APIView
from .models import CarMake
from .serializers import CarMakeSerializer
from rest_framework import status
from rest_framework.response import Response


class CarMakeAPI(APIView):
    def get(self, request):
        carmakes = CarMake.objects.all()
        if not carmakes.exists():
            return Response(
                {"message": "No car makes available."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CarMakeSerializer(carmakes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
