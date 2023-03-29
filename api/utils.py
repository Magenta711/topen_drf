from api.models import *
import uuid

class Utils:
    def reset_password_email(request, current_date):
        email = request.data.get('email')
        token = uuid.uuid4()

        generated_token = PasswordResets()
        generated_token.created_at = current_date
        generated_token.token = token
        generated_token.email = email
        generated_token.save()

        return token
        
    def token_validation_email(request):
        token = request.data.get('token')
        PasswordResets.objects.get(token = token)
        
    def change_password_email(request):
        token = request.data.get('token')
        password = request.data.get('password')
        password_resets = PasswordResets.objects.get(token = token)
        user = User.objects.get(username = password_resets.email)
        user.set_password(password)
        user.save()
        password_resets.delete()