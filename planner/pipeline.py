
def user_update_handler(request, details, social, uid, user, is_new, **kwargs):

    extra = social.extra_data or {}

    player = details.get('player') or {}

    extra['avatar'] = player.get('avatar')
    extra['nick'] = player.get('personaname')
    extra['profileurl'] = player.get('profileurl')

    social.extra_data = extra
    social.save()
