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
    天气查询接口
    接收 city 参数，调用 wttr.in API 获取天气信息
    返回实时气温和天气描述
    """
    city = request.args.get('city', '').strip()
    
    if not city:
        return jsonify({
            'success': False,
            'error': '城市参数不能为空'
        }), 400
    
    try:
        # 调用 wttr.in API
        url = f'https://wttr.in/{city}?format=j1'
        response = requests.get(url, timeout=10)
        
        # 检查请求是否成功
        if response.status_code != 200:
            return jsonify({
                'success': False,
                'error': f'天气服务请求失败，状态码: {response.status_code}'
            }), 500
        
        # 解析 JSON 响应
        weather_data = response.json()
        
        # 提取当前天气信息
        current_condition = weather_data.get('current_condition', [])
        if not current_condition:
            return jsonify({
                'success': False,
                'error': '无法获取天气数据'
            }), 500
        
        current = current_condition[0]
        
        # 提取气温和天气描述
        temperature = current.get('temp_C', 'N/A')
        weather_desc = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
        
        return jsonify({
            'success': True,
            'data': {
                'city': city,
                'temperature': temperature,
                'description': weather_desc
            }
        }), 200
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'请求天气服务时发生错误: {str(e)}'
        }), 500
    except (KeyError, IndexError, ValueError) as e:
        return jsonify({
            'success': False,
            'error': f'解析天气数据时发生错误: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'未知错误: {str(e)}'
        }), 500



