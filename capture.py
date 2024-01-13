from typing import Callable

class Capture:


    def __init__(self, live_id):
        self.live_id = live_id

        self._on_chat_message: Callable | None = None
        self._on_like_message: Callable | None = None
        self._on_member_message: Callable | None = None
        self._on_gift_message: Callable | None = None
        self._on_social_message: Callable | None = None
        self._on_room_user_seq_message: Callable | None = None
        self._on_update_fan_ticket_message: Callable | None = None
        self._on_common_text_message: Callable | None = None
        self._on_product_change_message: Callable | None = None 
        self._on_fansclub_message: Callable | None = None
        self._on_control_message: Callable | None = None

    def start(self):
        pass
    
    async def async_start(self):
        pass

    def stop(self):
        pass

    # region Callbacks
    
    def on_chat_message(self, message: dict):
        if self._on_chat_message:
            self._on_chat_message(message)

    def on_like_message(self, message: dict):
        if self._on_like_message:
            self._on_like_message(message)

    def on_member_message(self, message: dict):
        if self._on_member_message:
            self._on_member_message(message)

    def on_gift_message(self, message: dict):
        if self._on_gift_message:
            self._on_gift_message(message)

    def on_social_message(self, message: dict):
        if self._on_social_message:
            self._on_social_message(message)

    def on_room_user_seq_message(self, message: dict):
        if self._on_room_user_seq_message:
            self._on_room_user_seq_message(message)

    def on_update_fan_ticket_message(self, message: dict):
        if self._on_update_fan_ticket_message:
            self._on_update_fan_ticket_message(message)

    def on_common_text_message(self, message: dict):
        if self._on_common_text_message:
            self._on_common_text_message(message)

    def on_product_change_message(self, message: dict):
        if self._on_product_change_message:
            self._on_product_change_message(message)

    def on_fansclub_message(self, message: dict):
        if self._on_fansclub_message:
            self._on_fansclub_message(message)

    def on_control_message(self, message: dict):
        if self._on_control_message:
            self._on_control_message(message)

    def set_on_chat_message(self, callback: Callable):
        self._on_chat_message = callback
    
    def set_on_like_message(self, callback: Callable):
        self._on_like_message = callback

    def set_on_member_message(self, callback: Callable):
        self._on_member_message = callback

    def set_on_gift_message(self, callback: Callable):
        self._on_gift_message = callback

    def set_on_social_message(self, callback: Callable):
        self._on_social_message = callback

    def set_on_room_user_seq_message(self, callback: Callable):
        self._on_room_user_seq_message = callback

    def set_on_update_fan_ticket_message(self, callback: Callable):
        self._on_update_fan_ticket_message = callback

    def set_on_common_text_message(self, callback: Callable):
        self._on_common_text_message = callback

    def set_on_product_change_message(self, callback: Callable):
        self._on_product_change_message = callback

    def set_on_fansclub_message(self, callback: Callable):
        self._on_fansclub_message = callback

    def set_on_control_message(self, callback: Callable):
        self._on_control_message = callback

    # endregion