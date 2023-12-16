import gzip
import re
import requests
from websocket import WebSocketApp
from capute import Caputre
from douyin.protobuf import dy_pb2

class DouYin(Caputre):
    
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
        self.ws = WebSocketApp(wss,
                        header=headers,
                        on_open=self._on_open,
                        on_message=self._on_message,
                        on_error=self._on_error,
                        on_close=self._on_close)
        try:
            self.ws.run_forever()
        except Exception:
            self.ws.close()
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
            return None, err

        ttwid = response.cookies.get_dict().get("ttwid")
        match = re.search(r'roomId\\":\\"(\d+)\\"', response.text)
        if match is None or len(match.groups()) < 1:
            print("DouYin: No match found for roomId")
            return None, err

        live_room_id = match.group(1)
        
        return ttwid, live_room_id
    
    def _on_open(self, ws):
        print("DouYin: WebSocket connection opened")

    def _on_message(self, ws, message):
        '''接收到消息'''
        frame = dy_pb2.PushFrame()
        frame.ParseFromString(message)
        origin_bytes = gzip.decompress(frame.payload)
        response = dy_pb2.Response()
        response.ParseFromString(origin_bytes)
        
        if response.needAck:
            ack_pack = dy_pb2.PushFrame()
            ack_pack.logId = frame.logId
            ack_pack.payloadType = response.internalExt

            self.ws.send(ack_pack.SerializeToString())
        
        for msg in response.messagesList:
            method = msg.method
            if method == 'WebcastChatMessage':
                self._parse_chat_msg(msg.payload)
            elif method == "WebcastGiftMessage":
                self._parse_gift_msg(msg.payload)
            elif method == "WebcastGiftMessage":
                self._parse_like_msg(msg.payload)
            elif method == "WebcastGiftMessage":
                self._parse_member_msg(msg.payload)

    def _on_error(self, ws, error):
        print("DouYin: WebSocket error: ", error)

    def _on_close(self, ws):
        print("DouYin: WebSocket connection closed")

    def _parse_chat_msg(self, payload):
        '''聊天消息'''
        message = dy_pb2.ChatMessage()
        message.ParseFromString(payload)

        user_name = message.user.nickName
        content = message.content
        print(f"{user_name}: {content}")

    def _parse_gift_msg(self, payload):
        '''礼物消息'''
        message = dy_pb2.GiftMessage()
        message.ParseFromString(payload)

        user_name = message.user.nickName
        gift_name = message.gift.name
        gift_cnt = message.comboCount
        print(f"{user_name} 送出了 {gift_name}x{gift_cnt}")

    def _parse_like_msg(self, payload):
        '''点赞消息'''
        message = dy_pb2.LikeMessage()
        message.ParseFromString(payload)

        user_name = message.user.nickName
        like_cnt = message.count
        print(f"{user_name} 点了{like_cnt}个赞")

    def _parse_member_msg(self, payload):
        '''进入直播间消息'''
        message = dy_pb2.MemberMessage()
        message.ParseFromString(payload)

        user_name = message.user.nickName
        print(f"{user_name} 进入了直播间")