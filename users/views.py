# users/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to access this endpoint
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        print(user)
        return Response({
            'user': serializer.data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def referrals(request):
    user_referral_code = request.user.referral_code
    if user_referral_code:
        referred_users = User.objects.filter(referral_code=user_referral_code)
        serializer = UserSerializer(referred_users, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "No referrals found."})