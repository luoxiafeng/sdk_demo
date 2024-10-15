import cv2
import time
import os
import sys
import subprocess
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from functools import wraps
from multiprocessing import Process,set_start_method
from flask_sqlalchemy import SQLAlchemy
sys.path.append(os.path.abspath('webssh/webssh'))
from main import make_handlers, make_app, app_listen, ssh_main

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///channels.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 可选，关闭修改追踪
db = SQLAlchemy(app)

class Channel(db.Model):
    __tablename__ = 'channels'

    channel_number = db.Column(db.Integer, primary_key=True)
    camera_name = db.Column(db.String(100))
    video_url = db.Column(db.String(200))
    status = db.Column(db.String(50))
# 模拟用户数据库
users = {'admin': 'password'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('basic_info'))
        else:
            return "用户名或密码错误", 401
    return render_template('login.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def basic_info():
    device_info = {
        'device_id': 'RJ-BMOX-000738FADB3FA8289232CA9F49C0329',
        'status': '已授权',
        'software_version': '0.0.54',
        'box_time': '2024-07-09 10:11:32',
        'storage_space': '10.8GB',
        'chip_temperature': '45 °C',
        'system_version': 'BM1684-16 2.7.0'
    }
    chart_data = {
        'timestamps': ['2024/7/9 10:11:16', '2024/7/9 10:11:21', '2024/7/9 10:11:26', '2024/7/9 10:11:31'],
        'cpu_usage': [5, 6, 6, 6],
        'tpu_usage': [50, 55, 55, 55],
        'chip_temp': [45, 45, 45, 45]
    }
    return render_template('basic_info.html', device_info=device_info, chart_data=chart_data)

@app.route('/channel_management')
@login_required
def channel_management():
    return render_template('channel_management.html')

@app.route('/task_management')
@login_required
def task_management():
    return render_template('task_management.html')

@app.route('/task_management/add', methods=['GET'])
@login_required
def add_task():
    video_sources = [
        '02 - rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/201',
        '03 - rtsp://admin:passw0rd@192.168.1.104:554/Streaming/Channels/301'
    ]
    algorithms = [
        '明烟明火检测', '口罩检测', '攀爬检测', '人脸识别', '人体骨骼', '非机动车停车', '区域车停禁停', '车牌识别',
        '小动物检测', '人员拥挤检测', '人数超员检测', '人数监控(人体)', '离岗检测', '翻越围栏', '区域入侵',
        '越线检测', '街道垃圾检测', '打架检测', '电梯电动车检测', '安全帽检测', '反光衣检测', '未穿长袖检测',
        '工服检测', '工作安全带', '抽烟打电话检测', '驾驶员注意力分析', '倒地检测V2', '睡岗检测', '安全帽检测V3'
    ]
    return render_template('add_task.html', video_sources=video_sources, algorithms=algorithms)

@app.route('/live_preview')
@login_required
def live_preview():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
    ]
    return render_template('live_preview.html', cameras=cameras)

@app.route('/nine_tables')
@login_required
def nine_tables():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
    ]
    return render_template('nine_tables.html', cameras=cameras)

@app.route('/alarm_management')
@login_required
def alarm_management():
    alarms = [
        {
            'id': '06',
            'video_channel': '02',
            'alarm_date': '2024-07-09 10:03:33',
            'report_address': 'http://192.168.1.106:5201/receive',
            'report_status': '上传失败',
            'alarm_content': '未佩戴口罩',
            'image_url': 'path_to_image1.jpg'
        },
        {
            'id': '06',
            'video_channel': '02',
            'alarm_date': '2024-07-09 09:35:06',
            'report_address': 'http://192.168.1.106:5201/receive',
            'report_status': '上传失败',
            'alarm_content': '未佩戴口罩',
            'image_url': 'path_to_image2.jpg'
        },
        {
            'id': '06',
            'video_channel': '02',
            'alarm_date': '2024-07-09 09:33:36',
            'report_address': 'http://192.168.1.106:5201/receive',
            'report_status': '上传失败',
            'alarm_content': '未佩戴口罩',
            'image_url': 'path_to_image3.jpg'
        }
    ]
    return render_template('alarm_management.html', alarms=alarms)

@app.route('/parameter_settings')
@login_required
def parameter_settings():
    parameters = [
        {'id': 'AlarmSignalSec', 'type': '系统参数', 'value': '3', 'description': '物理告警信号输出持续时间(默认3秒)'},
        {'id': 'AudioVolume', 'type': '系统参数', 'value': '100', 'description': '系统音量（默认80,0~100）'},
        {'id': 'DimOfAlarmImage', 'type': '系统参数', 'value': '1', 'description': '告警图片尺寸大小（0宽高640×360,1原始相机尺寸，默认0）'},
        {'id': 'EnableAlarmNotification', 'type': '系统参数', 'value': '1', 'description': '是否开启网页告警通知(默认0,不开启)'},
        {'id': 'EnableAlarmSignal', 'type': '系统参数', 'value': '1', 'description': '是否开启物理OUT1告警信号(默认1,开启)'},
        {'id': 'EnableAlarmVoice', 'type': '系统参数', 'value': '1', 'description': '是否开启语音报警（需要手动添加语音音包，默认0不开启）'}
    ]
    return render_template('parameter_settings.html', parameters=parameters)

# 全局变量，用于存储当前正在播放的视频流地址
current_streams = {}

# 根据给定的视频流地址生成视频帧
def generate_frames(video_url):
    cap = cv2.VideoCapture(video_url)
    while True:
        success, frame = cap.read()
        time.sleep(0.020)
        if not success:
            time.sleep(0.002)
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    cap.release()

# 动态路由，根据摄像头ID返回对应的视频流
@app.route('/video/<nine_grid_id>')
@login_required
def video(nine_grid_id):
    video_url = current_streams.get(nine_grid_id)
    if video_url:
        return Response(generate_frames(video_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Video stream not found", 404

# 处理前端发送的请求，启动视频流
@app.route('/start-stream', methods=['POST'])
@login_required
def start_stream():
    data = request.get_json()
    nine_grid_id = data.get('nine_grid_id')
    video_url = data.get('video_url')

    if nine_grid_id and video_url:
        current_streams[nine_grid_id] = video_url
        return jsonify(success=True, stream_url=f'/video/{nine_grid_id}')
    else:
        return jsonify(success=False, message='Invalid channel ID or video URL')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': '没有上传文件'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400

    # 保存文件到上传文件夹
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'message': '文件上传成功'}), 200

@app.route('/check_video_status', methods=['POST'])
def check_video_status():
    data = request.json
    video_url = data.get('url')

    # 检查码流
    if check_stream(video_url):
        return jsonify(status='normal')

    # 如果没有码流，检查URL是否可访问
    if is_url_accessible(video_url):
        return jsonify(status='no_stream')
    
    return jsonify(status='network')

def check_stream(video_url):
    try:
        # 使用ffmpeg命令检测码流
        result = subprocess.run(
            ['ffmpeg', '-i', video_url],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        output = result.stderr.decode('utf-8')

        # 检查ffmpeg的返回码
        if result.returncode == 0:
            return True  # 成功获取流

        # 检查输出中是否有有效的流信息
        if "Invalid data" in output or "Could not find codec parameters" in output:
            return False  # 无效流

        # 根据输出的最后一行判断流的有效性
        lines = output.strip().split('\n')
        last_line = lines[-1]

        if "Error" in last_line or "failed" in last_line:
            return False  # 检测到错误

        return True  # 默认返回为有效流

    except Exception as e:
        print(f"Error checking stream: {e}")
        return False

def is_url_accessible(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.ConnectionError:
        print(f"Connection error for URL: {url}")
        return False
    except requests.Timeout:
        print(f"Timeout error for URL: {url}")
        return False
    except requests.RequestException as e:
        print(f"Request exception for URL: {url}, error: {e}")
        return False

@app.route('/submit_channels', methods=['POST'])
def submit_channels():
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效数据'}), 400

    for channel in data:
        channel_number = channel.get('channelNumber')
        camera_name = channel.get('cameraName')
        video_url = channel.get('videoUrl')
        status = channel.get('status')

        existing_channel = Channel.query.get(channel_number)

        if existing_channel:
            existing_channel.camera_name = camera_name
            existing_channel.video_url = video_url
            existing_channel.status = status
        else:
            new_channel = Channel(
                channel_number=channel_number,
                camera_name=camera_name,
                video_url=video_url,
                status=status
            )
            db.session.add(new_channel)

    try:
        db.session.commit()
        return jsonify({'message': '数据提交成功！'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def run_ssh_main():
    ssh_main()

def run_flask_app():
    UPLOAD_FOLDER = 'uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)

if __name__ == '__main__':
    with app.app_context():  # 在应用上下文中创建表
        db.create_all()  # 创建所有表
    #set_start_method('spawn')  # 确保在 Windows 上使用 spawn 方法
    #p1 = Process(target=run_ssh_main)
    p2 = Process(target=run_flask_app)

    #p1.start()
    p2.start()

    #p1.join()
    p2.join()
    
