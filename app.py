from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests

app = Flask(__name__)
# 开启 CORS，允许跨域请求
CORS(app)

# 模拟数据库：用户数据库
users_db = {
    '13800138001': {
        'phone': '13800138001',
        'name': '张三',
        'uid': '1001'
    }
}

# 模拟数据库：风控记录数据库（使用列表存储）
risk_db = []


@app.route('/api/user/search', methods=['GET'])
def search_user():
    """
    用户搜索接口
    接收 query 参数（手机号），返回用户信息
    """
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': '查询参数不能为空'}), 400
    
    # 在模拟数据库中查找用户
    user = users_db.get(query)
    
    if user:
        return jsonify({
            'success': True,
            'data': user
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': '未找到该用户'
        }), 404


@app.route('/api/risk', methods=['POST'])
def create_risk():
    """
    创建风控记录接口
    接收 JSON 数据，保存到模拟数据库
    """
    data = request.json
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 创建风控记录，添加创建时间
    risk_record = {
        'id': len(risk_db) + 1,
        'phone': data.get('phone', ''),
        'name': data.get('name', ''),
        'punishment': data.get('punishment', ''),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 保存到模拟数据库
    risk_db.append(risk_record)
    
    return jsonify({
        'success': True,
        'data': risk_record
    }), 201


@app.route('/api/risk', methods=['GET'])
def get_risk_list():
    """
    获取风控记录列表接口
    返回所有风控记录
    """
    return jsonify({
        'success': True,
        'data': risk_db
    }), 200


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """
    天气查询接口（Mock 数据版本）
    """
    city = request.args.get('city', '').strip()
    
    if not city:
        return jsonify({
            'success': False,
            'error': '城市参数不能为空'
        }), 400

    # Mock 固定返回数据（不再请求外部网络）
    return jsonify({
        'success': True,
        'data': {
            'city': city,
            'temperature': '26',
            'description': '晴转多云'
        }
    }), 200
    """
    本地 Mock 天气接口，不调用外部服务
    保持与之前相同的路径和参数：
    - 路径：/api/weather
    - 参数：city（查询字符串）
    """
    city = request.args.get('city', '').strip()

    # 参数校验
    if not city:
        return jsonify({
            "success": False,
            "error": "城市参数不能为空"
        }), 400

    # 固定返回的 Mock 数据
    return jsonify({
        "success": True,
        "data": {
            "city": city,
            "temperature": "26",
            "description": "晴转多云"
        }
    }), 200



