from .models import UserActivateTokens
from django.http import HttpResponse


def activate_user(request, activate_token):
    activated_user = UserActivateTokens.objects.activate_user_by_token(
        activate_token)
    if hasattr(activated_user, 'is_active'):
        if activated_user.is_active:
            message = 'ユーザーのアクティベーションが完了しました'
        if not activated_user.is_active:
            message = 'アクティベーションが失敗しています。管理者に問い合わせてください'
    if not hasattr(activated_user, 'is_active'):
        message = 'エラーが発生しました'
    return HttpResponse(message)