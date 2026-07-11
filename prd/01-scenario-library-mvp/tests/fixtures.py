def valid_scene():
    return {
        "scene_id": "SCN-001",
        "title": "雨夜路口行人侵入",
        "summary": "雨夜城市路口，自车接近人行横道时，一名行人从停靠车辆后方突然进入车道。系统发出制动请求，但首次识别略有延迟。",
        "environment": {
            "weather": "中雨",
            "lighting": "夜间",
            "road_type": "城市路口",
            "surface": "湿滑",
        },
        "actors": ["自车", "行人", "停靠车辆"],
        "trigger": "行人从停靠车辆后方突然进入自车道",
        "system_behavior": "系统识别行人后发出制动请求",
        "expected_behavior": "提前减速并为遮挡区域保留制动余量",
        "risk": "遮挡与低照度叠加导致识别延迟",
        "evidence": ["前视记录显示行人在进入车道前被车辆遮挡", "控制记录显示制动请求晚于目标窗口"],
        "tags": ["雨夜", "行人", "遮挡"],
        "synthetic": True,
        "source_basis": "method-only",
    }


def valid_query():
    return {
        "query_id": "Q-G-001",
        "text": "寻找雨夜被车辆遮挡后突然进入道路的行人场景",
        "query_type": "two-condition",
        "relevance": {"SCN-001": 3},
        "answerable": True,
    }
