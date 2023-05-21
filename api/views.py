from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


# Create your views here.
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        print(code)
        if code:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found' : 'Invalid Roomcode'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code Parameter Not Found in Request'}, status=status.HTTP_400_BAD_REQUEST)

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, reqeust, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            votes_to_skip = serializer.data.get('votes_to_skip')
            guest_can_pause = serializer.data.get('guest_can_pause')
            host = self.request.session.session_key

            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.votes_to_skip = votes_to_skip
                room.guest_can_pause = guest_can_pause
                self.request.session['room_code'] = room.code
                room.save(update_fields=['votes_to_skip', 'guest_can_pause'])
            else:
                room = Room(votes_to_skip=votes_to_skip, guest_can_pause=guest_can_pause, host=host)
                self.request.session['room_code'] = room.code
                print(room.code)
                print(guest_can_pause)
                print(votes_to_skip)
                room.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

class JoinRoom(APIView):
    lookup_code = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_code)
        if code:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                room = room[0]
                self.request.session['room_code'] = code
                return Response({'Message':'Room Joined successfully'}, status=status.HTTP_200_OK)
            return Response({'Bad Request':'Invalid Room Code Entered'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'No code entered'}, status=status.HTTP_400_BAD_REQUEST)

class CheckUserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = {
            'code' : self.request.session.get('room_code'),
        }
        return JsonResponse(data, status=status.HTTP_200_OK)

class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            code = self.request.session.pop('room_code')
            user_key = self.request.session.session_key
            user_room = Room.objects.filter(host=user_key)
            if len(user_room) > 0:
                user_room = user_room[0]
                user_room.delete()
        return Response({'Message': 'Delete Successful'}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            votes_to_skip = serializer.data.get('votes_to_skip')
            guest_can_pause = serializer.data.get('guest_can_pause')
            code = serializer.data.get('code')
        room = Room.objects.filter(code=code)
        if room.exists():
            room = room[0]
            user_id = request.session.session_key
            if user_id != room.host:
                return Response({"MSG":"Only host can change settings"}, status=status.HTTP_403_FORBIDDEN)
            room.votes_to_skip = votes_to_skip
            room.guest_can_pause = guest_can_pause
            room.save(update_fields=['votes_to_skip', 'guest_can_pause'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        else:
            return Response({"MSG":"Room doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
