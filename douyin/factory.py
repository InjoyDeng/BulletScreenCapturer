# warning: 目前是临时的数据结构，未来完成微信直播后会统一数据结构

def chat_message_wrapping(chat_message):
    user = chat_message.user
    return {
        "channel": "douyin",
        "type": "chat",
        "user": user_wrapping(user),
        "content": chat_message.content
    }

def gift_message_wrapping(gift_message):
    user = gift_message.user
    return {
        "channel": "douyin",
        "type": "gift",
        "user": user_wrapping(user),
        "gift": {
            "id": gift_message.gift.id,
            "name": gift_message.gift.name
        },
        "count": gift_message.total_count
    }

def like_message_wrapping(like_message):
    user = like_message.user
    return {
        "channel": "douyin",
        "type": "like",
        "user": user_wrapping(user),
        "count": like_message.count
    }

def member_message_wrapping(member_message):
    user = member_message.user
    return {
        "channel": "douyin",
        "type": "member",
        "user": user_wrapping(user)
    }

def social_message_wrapping(social_message):
    user = social_message.user
    return {
        "channel": "douyin",
        "type": "social",
        "user": user_wrapping(user)
    }

def room_user_seq_message_wrapping(room_user_seq_message):
    return {
        "channel": "douyin",
        "type": "state",
        "current": room_user_seq_message.total,
        "total": room_user_seq_message.total_pv_for_anchor
    }

def fansclub_message_wrapping(fansclub_message):
    return {
        "channel": "douyin",
        "type": "fansclub",
        "content": fansclub_message.content
    }

def control_message_wrapping(control_message):
    return {
        "channel": "douyin",
        "type": "control",
        "status": control_message.status
    }

def user_wrapping(user):
    return {
        "id": user.id,
        "short_id": user.short_id,
        "nick_name": user.nick_name,
        "display_id": user.display_id,
        "birthday": user.birthday,
        "level": user.level,
        "city": user.city,
    }