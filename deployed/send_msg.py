def handler(params):
    from wxauto import WeChat

    # 校验参数
    if not isinstance(params, dict):
        raise ValueError("参数必须为 JSON 对象")

    if "to" not in params:
        raise ValueError("缺少参数：to（接收人）")

    if "msg" not in params:
        raise ValueError("缺少参数：msg（消息内容）")

    to = params["to"]
    msg = params["msg"]

    if not isinstance(to, str) or not to.strip():
        raise ValueError("参数 'to' 必须是非空字符串")

    if not isinstance(msg, str) or not msg.strip():
        raise ValueError("参数 'msg' 必须是非空字符串")

    # 执行发送
    try:
        wx = WeChat()
        wx.SendMsg(msg, to)
        print(f"✅ 消息已发送：{msg} → {to}")
    except Exception as e:
        raise RuntimeError(f"发送失败：{str(e)}")