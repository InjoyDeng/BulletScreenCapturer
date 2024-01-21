import gzip, re, datetime, os
import requests, websocket
from capture import Capture
from douyin.protobuf.mapping import *

class DouYin(Capture):
    
    def start(self):
        ttwid, room_id = self._get_room_info()
        self._connect_web_socket(ttwid, room_id)
    
    def stop(self):
        self.ws.close()

    def _connect_web_socket(self, ttwid, room_id):
        '''连接 WebSocket'''
        wss = f"wss://webcast3-ws-web-lq.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.3.0&update_version_code=1.3.0&compress=gzip&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:{room_id}|dim_log_id:202302171547011A160A7BAA76660E13ED|fetch_time:1676620021641|seq:1|wss_info:0-1676620021641-0-0|wrds_kvs:WebcastRoomStatsMessage-1676620020691146024_WebcastRoomRankMessage-1676619972726895075_AudienceGiftSyncData-1676619980834317696_HighlightContainerSyncData-2&cursor=t-1676620021641_r-1_d-1_u-1_h-1&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&debug=false&endpoint=live_pc&support_wrds=1&im_path=/webcast/im/fetch/&user_unique_id={room_id}&device_platform=web&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh&browser_platform=MacIntel&browser_name=Mozilla&browser_version=5.0%20(Macintosh;%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/110.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&identity=audience&room_id={room_id}&heartbeatDuration=0&signature=00000000"
        headers = {
            "cookie": f"ttwid={ttwid}",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        self.ws = websocket.WebSocketApp(wss,
                        header=headers,
                        on_open=self._ws_on_open,
                        on_message=self._ws_on_message,
                        on_error=self._ws_on_error,
                        on_close=self._ws_on_close)
        try:
            self.ws.run_forever()
        except Exception:
            self.stop()
            raise
        
    def _get_room_info(self):
        '''获取直播间信息'''
        url = "https://live.douyin.com/" + self.live_id
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "cookie": "__ac_nonce=0123456789abcdef00000",
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as err:
            print("DouYin: request the live url error: ", err)
            raise

        ttwid = response.cookies.get_dict().get("ttwid")
        match = re.search(r'roomId\\":\\"(\d+)\\"', response.text)
        if match is None or len(match.groups()) < 1:
            response_file = datetime.datetime.now().strftime("log/dy_roominfo_%Y%m%d%H%M%S") + ".log"
            os.makedirs(os.path.dirname(response_file), exist_ok=True)
            with open(response_file, "w") as f:
                f.write(response.text)
            print("DouYin: No match found for roomId, result of request for room information has been written to: " + response_file)
            raise Exception("No match found for roomId")

        live_room_id = match.group(1)
        
        return ttwid, live_room_id
    
    def _ws_on_open(self, ws):
        print("DouYin: WebSocket connection opened")

    def _ws_on_message(self, ws, message):
        '''接收到消息'''
        package = PushFrame().parse(message)
        response = Response().parse(gzip.decompress(package.payload))
        
        if response.need_ack:
            ack = PushFrame(log_id=package.log_id,
                            payload_type='ack',
                            payload=response.internal_ext.encode('utf-8')
                            ).SerializeToString()
            ws.send(ack, websocket.ABNF.OPCODE_BINARY)
        
        for msg in response.messages_list:
            method = msg.method

            if method == 'WebcastChatMessage':
                # 聊天消息
                self._parse_chat_msg(msg.payload)

            elif method == "WebcastGiftMessage":
                # 礼物消息
                self._parse_gift_msg(msg.payload)

            elif method == "WebcastLikeMessage":
                # 点赞消息
                self._parse_like_msg(msg.payload)

            elif method == "WebcastMemberMessage":
                # 进入直播间消息
                self._parse_member_msg(msg.payload)

            elif method == "WebcastSocialMessage":
                # 关注消息
                self._parse_social_msg(msg.payload)

            elif method == "WebcastRoomUserSeqMessage":
                # 直播间统计
                self._parse_room_user_seq_msg(msg.payload)

            elif method == "WebcastFansclubMessage":
                # 粉丝团消息
                self._parse_fansclub_msg(msg.payload)

            elif method == "WebcastControlMessage":
                # 直播间状态消息
                self._parse_control_msg(msg.payload)


    def _ws_on_error(self, ws, error):
        print("DouYin: WebSocket error: ", error)

    def _ws_on_close(self, ws):
        print("DouYin: WebSocket connection closed")

    def _parse_chat_msg(self, payload):
        '''聊天消息'''
        message = ChatMessage().parse(payload)
        user_name = message.user.nick_name
        content = message.content
        print(f"{user_name}: {content}")

    def _parse_gift_msg(self, payload):
        '''礼物消息'''
        message = GiftMessage().parse(payload)
        user_name = message.user.nick_name
        gift_name = message.gift.name
        gift_cnt = message.combo_count
        print(f"{user_name} 送出了 {gift_name}x{gift_cnt}")

    def _parse_like_msg(self, payload):
        '''点赞消息'''
        message = LikeMessage().parse(payload)
        user_name = message.user.nick_name
        count = message.count
        print(f"{user_name} 点了{count}个赞")

    def _parse_member_msg(self, payload):
        '''进入直播间消息'''
        message = MemberMessage().parse(payload)
        user_name = message.user.nick_name
        print(f"{user_name} 进入了直播间")

    def _parse_social_msg(self, payload):
        '''关注消息'''
        message = SocialMessage().parse(payload)
        user_name = message.user.nick_name
        print(f"{user_name} 关注了主播")

    def _parse_room_user_seq_msg(self, payload):
        '''直播间统计'''
        message = RoomUserSeqMessage().parse(payload)
        current = message.total
        total = message.total_pv_for_anchor
        print(f"当前观看人数: {current}, 累计观看人数: {total}")

    def _parse_fansclub_msg(self, payload):
        '''粉丝团消息'''
        message = FansclubMessage().parse(payload)
        content = message.content
        print(f"粉丝团消息: {content}")

    def _parse_control_msg(self, payload):
        '''直播间状态消息'''
        message = ControlMessage().parse(payload)

        if message.status == 3:
            print("直播间已结束")
            self.stop()