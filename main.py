import sys
from server import Server
from printer import Printer
from douyin.douyin import DouYin



if __name__ == "__main__":
    # 获取运行参数
    arguments = sys.argv
    live_room_id = None
    if len(arguments) == 1 :
        print("运行参数中没有直播间ID，默认使用控制台输出消息。")
        print("如需开启 WebSocket 服务器转发消息，请在运行参数中加入直播间ID。例：python main.py 80017709309\n")
        print("可测试的直播间ID 东方甄选：80017709309 叫个朋友：168465302284")
        live_room_id = input("输入直播间ID: ")

        printer = Printer()
        dy = DouYin(live_room_id)
        printer.add_capture(dy)
        printer.start()
    else:
        live_room_id = arguments[1]
        print(f"直播间ID: {live_room_id}，开启 WebSocket 服务器转发消息")
        
        dy = DouYin(live_room_id)
        server = Server("0.0.0.0", 12321)
        server.add_capture(dy)
        server.run()