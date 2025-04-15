import os
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

DEPLOY_DIR = "deployed"
LOG_DIR = "logs"
REGISTRY_FILE = "registry.json"
PORT = 5001

os.makedirs(DEPLOY_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# 加载注册表
if os.path.exists(REGISTRY_FILE):
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)
else:
    registry = {}

# 保存注册表
def save_registry():
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

# 写入日志
def write_log(name, content):
    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(LOG_DIR, f"{name}_{ts}.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(content)

# 部署函数（注册）
@app.route("/deploy", methods=["POST"])
def deploy():
    data = request.json
    name = data.get("name")
    code = data.get("code")
    runtime = data.get("runtime", "direct")
    meta = data.get("meta", {})

    if not name or not code:
        return {"error": "缺少 name 或 code"}, 400

    file_path = os.path.join(DEPLOY_DIR, f"{name}.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    registry[name] = {
        "runtime": runtime,
        "meta": meta
    }
    save_registry()
    return {"status": "deployed", "function": name}

# 调用函数
@app.route("/invoke/<name>", methods=["POST"])
def invoke(name):
    file_path = os.path.join(DEPLOY_DIR, f"{name}.py")
    if not os.path.exists(file_path):
        return {"error": f"函数 {name} 不存在"}, 404

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    params = request.json or {}
    global_scope = {}
    output = ""

    try:
        from io import StringIO
        import sys
        stdout_backup = sys.stdout
        sys.stdout = mystdout = StringIO()

        exec(code, global_scope)
        handler = global_scope.get("handler")
        if callable(handler):
            handler(params)
        else:
            print("❌ handler(params) 未定义")

        sys.stdout = stdout_backup
        output = mystdout.getvalue()
    except Exception as e:
        sys.stdout = stdout_backup
        output = f"❌ 执行异常: {str(e)}"

    write_log(name, output)
    return {"status": "executed", "output": output}

# 查看已部署函数
@app.route("/list", methods=["GET"])
def list_functions():
    return {"functions": list(registry.keys())}

# 查看最近日志
@app.route("/logs", methods=["GET"])
def get_logs():
    files = sorted(os.listdir(LOG_DIR), reverse=True)
    if not files:
        return {"log": "暂无日志"}
    with open(os.path.join(LOG_DIR, files[0]), "r", encoding="utf-8") as f:
        return {"log": f.read()}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
