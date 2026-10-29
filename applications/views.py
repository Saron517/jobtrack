from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .serializers import ApplicationSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def application_list(request):
    # GET: show all of MY applications
    if request.method == "GET":
        applications = Application.objects.filter(owner=request.user).order_by("-created_at")
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    # POST: add a new application for ME
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def application_detail(request, pk):
    # Find this application, but only if it's MINE (otherwise 404)
    application = get_object_or_404(Application, pk=pk, owner=request.user)

    # GET: show one application
    if request.method == "GET":
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    # PATCH: change some fields
    if request.method == "PATCH":
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: remove it
    application.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)