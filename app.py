from flask import Flask, render_template,Response,request, jsonify
import cv2
app = Flask(__name__)

@app.route('/')
def dashboard():
    device_info = {
        'device_id': 'RJ-BMOX-000738FADB3FA8289232CA9F49C0329',
        'status': '已授权',
        'software_version': '0.0.54',
        'box_time': '2024-07-09 10:11:32',
        'storage_space': '10.8GB',
        'chip_temperature': '45 °C',
        'system_version': 'BM1684-16 2.7.0'
    }
    
    # Data for charts
    chart_data = {
        'timestamps': ['2024/7/9 10:11:16', '2024/7/9 10:11:21', '2024/7/9 10:11:26', '2024/7/9 10:11:31'],
        'cpu_usage': [5, 6, 6, 6],
        'tpu_usage': [50, 55, 55, 55],
        'chip_temp': [45, 45, 45, 45]
    }
    
    return render_template('dashboard.html', device_info=device_info, chart_data=chart_data)
@app.route('/channel_management')
def channel_management():
    channels = [
        {'camera_id': '005', 'video_url': 'rtsp://192.168.1.106:8554/test_stream', 'status': '连接视频失败', 'national_channel_id': '', 'operation': '编辑'},
        {'camera_id': '01', 'video_url': 'rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/101', 'status': '正常', 'national_channel_id': '', 'operation': '编辑'},
        {'camera_id': '02', 'video_url': 'rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/201', 'status': '正常', 'national_channel_id': '', 'operation': '编辑'},
        {'camera_id': '03', 'video_url': 'rtsp://admin:passw0rd@192.168.1.103:554/Streaming/Channels/301', 'status': '视频流不存在', 'national_channel_id': '', 'operation': '编辑'},
    ]
    
    return render_template('channel_management.html', channels=channels)

@app.route('/task_management')
def task_management():
    tasks = [
        {'task_id': '001', 'video_source': '02', 'report_address': '明烟明火检测, 口罩检测, 爬爬检测', 'algorithm_info': ['明烟明火检测', '口罩检测', '爬爬检测'], 'status': '未运行'},
        {'task_id': '002', 'video_source': '02', 'report_address': '安全帽检测, 反光衣检测, 未穿长袖检测', 'algorithm_info': ['安全帽检测', '反光衣检测', '未穿长袖检测'], 'status': '未运行'},
        {'task_id': '003', 'video_source': '02', 'report_address': '人员拥挤检测, 口罩检测, 反光衣检测', 'algorithm_info': ['人员拥挤检测', '口罩检测', '反光衣检测'], 'status': '未运行'},
        {'task_id': '004', 'video_source': '02', 'report_address': '脸部抓拍, 打架检测, 街道垃圾检测', 'algorithm_info': ['脸部抓拍', '打架检测', '街道垃圾检测'], 'status': '未运行'},
        {'task_id': '0045', 'video_source': '02', 'report_address': '越线检测, 安全帽检测, 反光衣检测', 'algorithm_info': ['越线检测', '安全帽检测', '反光衣检测'], 'status': '未运行'},
        {'task_id': '006', 'video_source': '02', 'report_address': '倒地检测V2, 安全帽检测V3', 'algorithm_info': ['倒地检测V2', '安全帽检测V3'], 'status': '未运行'},
    ]
    
    return render_template('task_management.html', tasks=tasks)

@app.route('/task_management/add', methods=['GET'])
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
def live_preview():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
    ]
    
    return render_template('live_preview.html', cameras=cameras)

@app.route('/nine_tables')
def nine_tables():
    cameras = [
        {'id': '01', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '02', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '03', 'status': '离线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
        {'id': '04', 'status': '在线', 'video_url': 'rtsp://192.168.57.16:8554/s10'},
    ]
    
    return render_template('nine_tables.html', cameras=cameras)

@app.route('/alarm_management')
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
        if not success:
            break
        else:
            # 转码至JPEG格式
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

# 动态路由，根据摄像头ID返回对应的视频流
@app.route('/video/<nine_grid_id>')
def video(nine_grid_id):
    # 获取对应摄像头ID的RTSP流地址
    video_url = current_streams.get(nine_grid_id)
    if video_url:
        return Response(generate_frames(video_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Video stream not found", 404

# 处理前端发送的请求，启动视频流
@app.route('/start-stream', methods=['POST'])
def start_stream():
    data = request.get_json()
    nine_grid_id = data.get('nine_grid_id')  # 获取通道号
    video_url = data.get('video_url')  # 获取前端传递的视频流地址

    # 检查是否有对应的通道号和视频地址
    if nine_grid_id and video_url:
        # 将通道号与视频地址存储到全局字典中
        current_streams[nine_grid_id] = video_url

        # 返回成功响应，并告知前端视频流的URL，可以用于动态设置img的src
        return jsonify(success=True, stream_url=f'/video/{nine_grid_id}')
    else:
        return jsonify(success=False, message='Invalid channel ID or video URL')


if __name__ == '__main__':
    # 使应用可以在局域网内访问
    app.run(host='0.0.0.0', port=5000, debug=True,threaded=True)
