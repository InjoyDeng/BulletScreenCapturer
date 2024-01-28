# BulletScreenCapturer

Tools to capture chat data from live streaming platforms

## Features

- [x] Support for DouYin live streaming.
- [x] WebSocket forwarding.
- [ ] Support for WeChat live streaming (in development).
- [ ] Standardization of data structures from different platforms (planned).

## Environment

 - Python >= 3.6

## Run

Please run the following command to create and activate the virtual environment:

```sh
python -m venv .venv

# For Linux and macOS
source .venv/bin/activate

# For Windows Command Prompt
.\.venv\Scripts\activate.bat

# For Windows PowerShell
.\.venv\Scripts\activate 
```

Then, install dependencies:
```sh
pip install -r requirements.txt
```

If everything works well, you can run the program in the way you need:

To output messages in the terminal, run the following command and enter a `liveId`:
```sh
python main.py
```

To run a **WebSocket server** and forward messages, you need to add `liveId` as an argument, like this:
```sh
python main.py 80017709309
```

## Credits

[Nats-ji/dy_danmu](https://github.com/Nats-ji/dy_danmu) for mapping `douyin.proto` to the Python class.