# BulletScreenCapturer

Tools to capture chat data from live streaming platforms

## Features

- [x] Support for DouYin live
- [ ] Support for WeChat live
- [ ] Standardize the data structure from different platforms
- [ ] WebSocket forward

## Run demo

please run the following command to create and activate the virtual environment:

```sh
python -m venv .venv

# linux and macos
source venv/bin/activate

# windows cmd
.\venv\Scripts\activate.bat

# windows powershell
.\venv\Scripts\activate 
```

Then, install dependencies:
```sh
pip install -r requirements.txt
```

You may want to edit the live id first.
```sh
python main.py
```

## Credits

[Nats-ji/dy_danmu](https://github.com/Nats-ji/dy_danmu) for mapping `douyin.proto` to the python class.