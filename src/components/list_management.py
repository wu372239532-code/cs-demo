from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# 模拟数据库
data = []

@app.route('/')
def index():
    # 获取查询参数
    payment_category = request.args.get('payment_category', '').strip()
    category_reviewer = request.args.get('category_reviewer', '').strip()
    project = request.args.get('project', '').strip()
    project_reviewer = request.args.get('project_reviewer', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    
    # 过滤数据
    filtered_data = data
    if payment_category:
        filtered_data = [d for d in filtered_data if payment_category.lower() in d.get('payment_category', '').lower()]
    if category_reviewer:
        filtered_data = [d for d in filtered_data if category_reviewer.lower() in d.get('reviewer', '').lower()]
    if project:
        filtered_data = [d for d in filtered_data if project.lower() in d.get('project', '').lower()]
    if project_reviewer:
        filtered_data = [d for d in filtered_data if project_reviewer.lower() in d.get('project_reviewer', '').lower()]
    if category:
        filtered_data = [d for d in filtered_data if category.lower() in d.get('category', '').lower()]
    if status:
        filtered_data = [d for d in filtered_data if d.get('status', '') == status]
    
    return render_template('index.html', data=filtered_data, 
                         payment_category=payment_category,
                         category_reviewer=category_reviewer,
                         project=project,
                         project_reviewer=project_reviewer,
                         category=category,
                         status=status)

@app.route('/add', methods=['POST'])
def add_entry():
    entry = {
        'id': len(data) + 1,
        'payment_category': request.form.get('payment_category', ''),
        'related_activity': request.form.get('related_activity', ''),
        'reviewer': request.form.get('reviewer', ''),
        'amount_limit': request.form.get('amount_limit', ''),
        'project': request.form.get('project', ''),
        'project_reviewer': request.form.get('project_reviewer', ''),
        'category': request.form.get('category', ''),
        'status': request.form.get('status', '启用'),
        'operator': request.form.get('operator', '系统管理员')
    }
    data.append(entry)
    return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entry = next((d for d in data if d['id'] == entry_id), None)
    if not entry:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        entry['payment_category'] = request.form.get('payment_category', '')
        entry['related_activity'] = request.form.get('related_activity', '')
        entry['reviewer'] = request.form.get('reviewer', '')
        entry['amount_limit'] = request.form.get('amount_limit', '')
        entry['project'] = request.form.get('project', '')
        entry['project_reviewer'] = request.form.get('project_reviewer', '')
        entry['category'] = request.form.get('category', '')
        entry['status'] = request.form.get('status', '启用')
        entry['operator'] = request.form.get('operator', '系统管理员')
        return redirect(url_for('index'))
    
    return render_template('edit.html', entry=entry)

@app.route('/disable/<int:entry_id>', methods=['POST'])
def disable_entry(entry_id):
    entry = next((d for d in data if d['id'] == entry_id), None)
    if entry:
        entry['status'] = '禁用'
        entry['operator'] = request.form.get('operator', '系统管理员')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 避免与项目里现有的 Flask 后端（常用 5000 端口）冲突，改用 5001
    app.run(host='127.0.0.1', port=5001, debug=True)