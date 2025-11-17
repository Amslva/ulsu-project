from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from ..models import UserProfile

class UserAvatarAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        avatar_type = request.data.get('avatar_type')
        
        # Получаем или создаём профиль
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'avatar_type': 'men'}  # значение по умолчанию
        )
        
        if avatar_type in ['men', 'girl']:
            profile.avatar_type = avatar_type
            profile.save()
            return Response({
                'message': 'Аватарка изменена', 
                'avatar_url': profile.get_avatar_url()
            })
        else:
            return Response({'error': 'Неверный тип аватарки'}, status=400)
        
class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Валидация
        if not current_password:
            return Response(
                {'error': 'Текущий пароль обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not new_password:
            return Response(
                {'error': 'Новый пароль обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not confirm_password:
            return Response(
                {'error': 'Подтверждение пароля обязательно'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем текущий пароль
        if not user.check_password(current_password):
            return Response(
                {'error': 'Текущий пароль неверен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем что новые пароли совпадают
        if new_password != confirm_password:
            return Response(
                {'error': 'Новые пароли не совпадают'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()
        
        # Обновляем сессию аутентификации (для админки)
        update_session_auth_hash(request, user)
        
        return Response({'message': 'Пароль успешно изменен'})


class RegisterAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response(
                {'error': 'Все поля обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Пользователь с таким именем уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Пользователь успешно создан',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })

        except Exception as e:
            return Response(
                {'error': f'Ошибка при создании пользователя: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username и пароль обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(username=username, password=password)

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Успешный выход'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            profile = user.profile
            avatar_url = profile.get_avatar_url()
        except UserProfile.DoesNotExist:
            avatar_url = '/avatars/men.png'
            
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar_url': avatar_url  # ← Добавляем URL аватарки
        })
    