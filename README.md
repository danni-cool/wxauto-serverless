# wxauto-serverless

`wxauto-serverless` 实现了一个极简的基于 Flask 的轻量级无服务器函数运行时，支持动态部署和调用 Python 函数。它还集成了日志记录功能，便于调试和监控。

## 功能

1. **动态部署函数**：通过 `/deploy` 接口上传和注册 Python 函数。
2. **调用已部署函数**：通过 `/invoke/<name>` 接口调用已注册的函数。
3. **查看已部署函数**：通过 `/list` 接口获取所有已注册函数的列表。
4. **日志管理**：通过 `/logs` 接口查看最近的执行日志。

## 文件结构

```
wxauto-serverless/
├── deployed/          # 存储已部署的函数代码
├── logs/              # 存储执行日志
├── main.py            # 主程序文件
├── registry.json      # 注册表文件，记录已部署函数的元信息
└── README.md          # 项目说明文件
```

## 接口说明

### 1. 部署函数

**URL**: `/deploy`  
**方法**: `POST`  
**参数**:
- `name` (字符串): 函数名称。
- `code` (字符串): 函数代码，需包含 `handler(params)` 函数。
- `runtime` (可选，字符串): 运行时环境，默认为 `direct`。
- `meta` (可选，JSON 对象): 函数的元信息。

**示例请求**:
```json
POST /deploy
{
  "name": "send_msg",
  "code": "def handler(params): print(params)",
  "runtime": "direct",
  "meta": {"description": "发送消息"}
}
```

**响应**:
```json
{
  "status": "deployed",
  "function": "send_msg"
}
```

---

### 2. 调用函数

**URL**: `/invoke/<name>`  
**方法**: `POST`  
**参数**: 函数的输入参数 (JSON 对象)。

**示例请求**:
```json
POST /invoke/send_msg
{
  "to": "Alice",
  "msg": "Hello, Alice!"
}
```

**响应**:
```json
{
  "status": "executed",
  "output": "✅ 消息已发送：Hello, Alice! → Alice"
}
```

---

### 3. 查看已部署函数

**URL**: `/list`  
**方法**: `GET`  

**响应**:
```json
{
  "functions": ["send_msg"]
}
```

---

### 4. 查看最近日志

**URL**: `/logs`  
**方法**: `GET`  

**响应**:
```json
{
  "log": "✅ 消息已发送：Hello, Alice! → Alice"
}
```

---

## 部署与运行

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/your-repo/wxauto-serverless.git
   cd wxauto-serverless
   ```

2. 安装依赖：
   ```bash
   pip install flask wxauto
   ```

3. 启动服务：
   ```bash
   python main.py
   ```

4. 服务将运行在 `http://0.0.0.0:5001`。

---

## 注意事项

- 部署的函数代码必须包含 `handler(params)` 函数作为入口。
- 日志文件存储在 `logs/` 目录下，按时间戳命名。
- 确保 `wxauto` 模块已正确安装并配置微信客户端。

---

## 示例函数

以下是一个示例函数 `send_msg`，用于通过微信发送消息：

```python
def handler(params):
    from wxauto import WeChat

    if "to" not in params或 "msg" not in params:
        raise ValueError("缺少必要参数：to 或 msg")

    wx = WeChat()
    wx.SendMsg(params["msg"], params["to"])
    print(f"✅ 消息已发送：{params['msg']} → {params['to']}")
```

将此代码通过 `/deploy` 接口上传后，即可通过 `/invoke/send_msg` 调用。

---

## 贡献

欢迎提交 Issue 和 Pull Request 来改进此项目！
