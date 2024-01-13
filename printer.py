class Printer:
    def __init__(self):
        self.captures = []

    def add_capture(self, capture):
        self.captures.append(capture)

        capture.set_on_chat_message(self._receive_chat_message)
        capture.set_on_like_message(self._receive_like_message)
        capture.set_on_member_message(self._receive_member_message)
        capture.set_on_gift_message(self._receive_gift_message)
        capture.set_on_social_message(self._receive_social_message)
        capture.set_on_room_user_seq_message(self._receive_room_user_seq_message)
        capture.set_on_update_fan_ticket_message(self._receive_update_fan_ticket_message)
        capture.set_on_common_text_message(self._receive_common_text_message)
        capture.set_on_product_change_message(self._receive_product_change_message)
        capture.set_on_fansclub_message(self._receive_fansclub_message)
        capture.set_on_control_message(self._receive_control_message)

    def start(self):
        for capture in self.captures:
            capture.start()

    def stop(self):
        for capture in self.captures:
            capture.stop()

    def _receive_chat_message(self, message: dict):
        user_name = message['user']['nick_name']
        content = message['content']
        print(f"{user_name}: {content}")

    def _receive_like_message(self, message: dict):
        user_name = message['user']['nick_name']
        count = message['count']
        print(f"{user_name} 点了{count}个赞")

    def _receive_member_message(self, message: dict):
        user_name = message['user']['nick_name']
        print(f"{user_name} 进入了直播间")

    def _receive_gift_message(self, message: dict):
        user_name = message['user']['nick_name']
        gift_name = message['gift']['name']
        total_count = message['count']
        print(f"{user_name} 送出了 {gift_name}x{total_count}")

    def _receive_social_message(self, message: dict):
        user_name = message['user']['nick_name']
        print(f"{user_name} 关注了主播")

    def _receive_room_user_seq_message(self, message: dict):
        current = message['current']
        total = message['total']
        print(f"当前观看人数: {current}, 累计观看人数: {total}")

    def _receive_update_fan_ticket_message(self, message: dict):
        pass

    def _receive_common_text_message(self, message: dict):
        pass

    def _receive_product_change_message(self, message: dict):
        pass

    def _receive_fansclub_message(self, message: dict):
        content = message['content']
        print(f"粉丝团消息: {content}")

    def _receive_control_message(self, message: dict):
        if message['status'] == 3:
            print("直播间已结束")
            self.stop()

        print(f"直播间状态消息: {message}")
        

