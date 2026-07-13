import base64
import os
import threading
import time
import webbrowser
from typing import Any

import requests
from flask import Flask, jsonify, request, send_file, send_from_directory
from werkzeug.utils import secure_filename

try:
    from flask_cors import CORS
except ImportError:  # pragma: no cover
    CORS = None


app = Flask(__name__)
if CORS is not None:
    CORS(app)

AGNES_API_KEY = os.getenv("AGNES_API_KEY", "here is your api key")
AGNES_BASE_URL = os.getenv("AGNES_BASE_URL", "https://apihub.agnes-ai.com")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
OUTPUT_IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
OUTPUT_VIDEO_DIR = os.path.join(OUTPUT_DIR, "videos")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_VIDEO_DIR, exist_ok=True)

GENERATION_HISTORY: list[dict[str, Any]] = []


def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def request_json(method: str, url: str, api_key: str, payload: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> requests.Response:
    headers = build_headers(api_key)
    try:
        return requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload,
            params=params,
            timeout=120,
            verify=False,
        )
    except requests.exceptions.RequestException as exc:
        raise requests.exceptions.RequestException(str(exc)) from exc


def query_video_status(api_key: str, video_id: str | None) -> dict[str, Any]:
    if not video_id:
        return {}
    try:
        response = requests.get(
            f"{AGNES_BASE_URL}/agnesapi",
            headers={"Authorization": f"Bearer {api_key}"},
            params={"video_id": video_id},
            timeout=120,
            verify=False,
        )
    except requests.exceptions.RequestException as exc:
        return {"status": "error", "error": str(exc)}
    if response.status_code >= 400:
        return {"status": "error", "error": response.text}
    try:
        return response.json()
    except ValueError:
        return {"status": "error", "error": response.text}


def append_history(entry: dict[str, Any]) -> None:
    GENERATION_HISTORY.append(entry)
    if len(GENERATION_HISTORY) > 20:
        GENERATION_HISTORY.pop(0)


def is_public_http_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    if not url.startswith(("http://", "https://")):
        return False
    lowered = url.lower()
    blocked_hosts = ("localhost", "127.0.0.1", "0.0.0.0", "::1")
    return not any(host in lowered for host in blocked_hosts)


def is_data_uri_base64(value: str) -> bool:
    if not value or not isinstance(value, str):
        return False
    return value.startswith("data:image/") and ";base64," in value


def normalize_image_input(value: str, mime: str = "image/png") -> str | None:
    if not value or not isinstance(value, str):
        return None
    trimmed = value.strip()
    if is_data_uri_base64(trimmed):
        return trimmed
    if trimmed.startswith(("http://", "https://")):
        return trimmed
    if trimmed.startswith("data:"):
        return trimmed
    # 纯 base64 字符串，补齐 Data URI 前缀
    if len(trimmed) > 64:
        return f"data:{mime};base64,{trimmed}"
    return None


def validate_image_inputs(values: list[str], field_name: str = "图片") -> tuple[list[str] | None, str | None]:
    if not values:
        return [], None
    normalized: list[str] = []
    for value in values:
        normalized_value = normalize_image_input(value)
        if not normalized_value:
            return None, f"{field_name} 格式无效，请提供公网 URL 或 Base64 / Data URI"
        if is_data_uri_base64(normalized_value):
            normalized.append(normalized_value)
            continue
        if is_public_http_url(normalized_value):
            normalized.append(normalized_value)
            continue
        return (
            None,
            f"{field_name} 必须是公网 URL，或 Base64 / Data URI（本地图片请先上传，系统会自动转换）。",
        )
    return normalized, None


def validate_public_image_urls(urls: list[str], field_name: str = "图片") -> str | None:
    _, error = validate_image_inputs(urls, field_name)
    return error


def is_error_payload(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    if payload.get("error"):
        return True
    if payload.get("detail"):
        return True
    if payload.get("message") and isinstance(payload.get("message"), str) and "invalid" in payload.get("message", "").lower():
        return True
    return False


def save_remote_asset(url: str, subdir: str, prefix: str) -> str | None:
    if not url or not isinstance(url, str):
        return None
    if not url.startswith("http"):
        return None
    target_dir = OUTPUT_IMAGE_DIR if subdir == "images" else OUTPUT_VIDEO_DIR
    extension = ".png" if subdir == "images" else ".mp4"
    filename = f"{prefix}_{int(time.time())}{extension}"
    save_path = os.path.join(target_dir, filename)
    try:
        with requests.get(url, stream=True, timeout=120, verify=False) as response:
            response.raise_for_status()
            with open(save_path, "wb") as handle:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        handle.write(chunk)
        return save_path
    except Exception:
        return None


def open_browser(url: str) -> None:
    try:
        webbrowser.open(url, new=0)
    except Exception:
        pass


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/outputs/videos/<path:filename>")
def output_video(filename: str):
    return send_from_directory(OUTPUT_VIDEO_DIR, filename)


@app.route("/api/samples", methods=["GET"])
def list_samples():
    samples = [
        {
            "id": "text-long",
            "title": "文生视频 · 18 秒",
            "mode": "text",
            "file": "video_task_7e0BkgnZTNAQ7jQcJUYcAvjaECHHXARs.mp4",
            "duration": "18.4s",
            "meta": "441帧 · 24fps · seed 43 · 1088×832",
            "description": "写实暗黑国风仙侠，含分镜式运镜描述",
        },
        {
            "id": "text-standard",
            "title": "文生视频 · 5 秒",
            "mode": "text",
            "file": "video_task_Q1HffJJB6mEyAykBxCqxCfu4el0zZJ4F_1783932308.mp4",
            "duration": "5.0s",
            "meta": "121帧 · 24fps · 默认配置",
            "description": "典型文生视频，纯文本输入快速出片",
        },
        {
            "id": "keyframes-local",
            "title": "关键帧动画 · 5 秒",
            "mode": "keyframes",
            "file": "video_task_Ro0HKUqg57ttpltA0z1iE4yAv4wiLMbw_1783935044.mp4",
            "duration": "5.0s",
            "meta": "本地上传 3 张 Base64 · 121帧 · 24fps",
            "description": "渐进式转场，本地截图关键帧动画",
        },
    ]
    available = []
    for item in samples:
        path = os.path.join(OUTPUT_VIDEO_DIR, item["file"])
        if os.path.isfile(path):
            available.append({**item, "url": f"/outputs/videos/{item['file']}"})
    return jsonify({"items": available})


@app.route("/health")
def health():
    return jsonify({"ok": True, "base": AGNES_BASE_URL})


@app.route("/api/upload/image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "请上传图片文件"}), 400

    uploaded = request.files["file"]
    if uploaded.filename == "":
        return jsonify({"error": "文件名不能为空"}), 400

    filename = f"{int(time.time())}_{secure_filename(uploaded.filename)}"
    save_path = os.path.join(UPLOAD_DIR, filename)
    uploaded.save(save_path)

    mime = uploaded.mimetype or "image/png"
    if not mime.startswith("image/"):
        mime = "image/png"
    with open(save_path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("ascii")
    data_uri = f"data:{mime};base64,{encoded}"

    public_url = request.host_url.rstrip("/") + "/uploads/" + filename
    return jsonify({"ok": True, "filename": filename, "url": public_url, "data_uri": data_uri})


@app.route("/api/agnes/history", methods=["GET"])
def agnes_history():
    return jsonify({"items": list(reversed(GENERATION_HISTORY))})


@app.route("/api/agnes/keyframes", methods=["POST"])
def agnes_keyframes():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "请输入关键帧描述"}), 400

    api_key = (data.get("api_key") or AGNES_API_KEY).strip()
    count = int(data.get("count", 3) or 3)
    count = max(1, min(count, 4))
    image_urls = data.get("image_urls") or data.get("images") or []
    body: dict[str, Any] = {
        "model": "agnes-image-2.0-flash",
        "prompt": prompt,
        "size": data.get("size", "1024x768"),
        "extra_body": {"response_format": "url"},
    }
    if image_urls:
        normalized_images, invalid = validate_image_inputs(image_urls, "参考图")
        if invalid:
            return jsonify({"error": invalid}), 400
        body["extra_body"]["image"] = normalized_images[:4]

    try:
        response = request_json("POST", f"{AGNES_BASE_URL}/v1/images/generations", api_key, payload=body)
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Agnes 请求失败: {exc}"}), 502

    if response.status_code >= 400:
        return jsonify({"error": response.text}), response.status_code

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    if is_error_payload(payload):
        return jsonify({"error": payload}), 502

    generated_items: list[dict[str, Any]] = []
    items = payload.get("data") if isinstance(payload, dict) else None
    if isinstance(items, list):
        for item in items[:count]:
            if isinstance(item, dict):
                url = item.get("url")
                if url:
                    local_path = save_remote_asset(url, "images", "keyframe")
                    generated_items.append({"url": url, "local_path": local_path})
    elif isinstance(payload, dict) and payload.get("url"):
        local_path = save_remote_asset(payload["url"], "images", "keyframe")
        generated_items.append({"url": payload["url"], "local_path": local_path})

    return jsonify({"items": generated_items, "count": len(generated_items)})


@app.route("/api/agnes/text", methods=["POST"])
def agnes_text():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "请输入文本描述"}), 400

    api_key = (data.get("api_key") or AGNES_API_KEY).strip()
    model = data.get("model") or "agnes-2.0-flash"
    body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": (
                    "你是一个视频生成提示词优化师。"
                    "请将下面的内容改写为更适合视频生成的英文提示词，"
                    "只输出一句话，不要解释。\n"
                    f"{prompt}"
                ),
            }
        ],
        "stream": False,
    }

    try:
        response = request_json("POST", f"{AGNES_BASE_URL}/v1/chat/completions", api_key, payload=body)
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Agnes 请求失败: {exc}"}), 502

    if response.status_code >= 400:
        return jsonify({"error": response.text}), response.status_code

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    if is_error_payload(payload):
        return jsonify({"error": payload}), 502

    content = ""
    try:
        content = payload["choices"][0]["message"]["content"]
    except Exception:
        content = str(payload)

    return jsonify({"content": content, "model": model})


@app.route("/api/agnes/video", methods=["POST"])
def agnes_video():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "请输入视频描述"}), 400

    api_key = (data.get("api_key") or AGNES_API_KEY).strip()
    mode = (data.get("mode") or "text").lower()
    body: dict[str, Any] = {
        "model": "agnes-video-v2.0",
        "prompt": prompt,
        "height": data.get("height", 768),
        "width": data.get("width", 1152),
        "num_frames": data.get("num_frames", 121),
        "frame_rate": data.get("frame_rate", 24),
    }

    if mode == "image" and data.get("image"):
        normalized_images, invalid = validate_image_inputs([data.get("image")], "参考图")
        if invalid:
            return jsonify({"error": invalid}), 400
        body["image"] = normalized_images[0]
    elif mode == "keyframes":
        keyframes = data.get("keyframes") or []
        if keyframes:
            normalized_images, invalid = validate_image_inputs(keyframes, "关键帧")
            if invalid:
                return jsonify({"error": invalid}), 400
            body["extra_body"] = {"image": normalized_images, "mode": "keyframes"}
        elif data.get("image"):
            normalized_images, invalid = validate_image_inputs([data.get("image")], "参考图")
            if invalid:
                return jsonify({"error": invalid}), 400
            body["image"] = normalized_images[0]

    if data.get("negative_prompt"):
        body["negative_prompt"] = data.get("negative_prompt")

    if data.get("seed") is not None and data.get("seed") != "":
        body["seed"] = int(data.get("seed"))

    if data.get("num_inference_steps") is not None and data.get("num_inference_steps") != "":
        body["num_inference_steps"] = int(data.get("num_inference_steps"))

    try:
        response = request_json("POST", f"{AGNES_BASE_URL}/v1/videos", api_key, payload=body)
    except requests.exceptions.RequestException as exc:
        return jsonify({"error": f"Agnes 请求失败: {exc}"}), 502

    if response.status_code >= 400:
        return jsonify({"error": response.text}), response.status_code

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text}

    if is_error_payload(payload):
        return jsonify({"error": payload}), 502

    task_id = payload.get("task_id") or payload.get("id")
    video_id = payload.get("video_id")

    if not task_id and not video_id:
        return jsonify({"error": "接口未返回可追踪的任务信息", "detail": payload}), 502

    final_payload: dict[str, Any] | None = None
    result_payload: dict[str, Any] = {}
    for attempt in range(120):
        if attempt > 0:
            time.sleep(5)
        result_payload = query_video_status(api_key, video_id or task_id)
        if result_payload.get("status") in {"completed", "succeeded"} and result_payload.get("url"):
            final_payload = result_payload
            break
        if result_payload.get("status") in {"failed", "error", "cancelled", "canceled"}:
            break

    latest = final_payload or result_payload or payload
    history_entry = {
        "prompt": prompt,
        "mode": mode,
        "task_id": task_id,
        "video_id": video_id,
        "status": latest.get("status", payload.get("status", "queued")),
        "url": latest.get("url"),
        "created_at": time.time(),
    }
    append_history(history_entry)

    if final_payload and final_payload.get("url"):
        local_path = save_remote_asset(final_payload.get("url"), "videos", f"video_{task_id or video_id or 'task'}")
        if local_path:
            final_payload["local_path"] = local_path
        return jsonify(
            {
                "task_id": task_id,
                "video_id": video_id,
                "status": final_payload.get("status"),
                "url": final_payload.get("url"),
                "seconds": final_payload.get("seconds"),
                "size": final_payload.get("size"),
                "local_path": local_path,
                "payload": final_payload,
            }
        )

    return jsonify(
        {
            "task_id": task_id,
            "video_id": video_id,
            "status": latest.get("status", "queued"),
            "progress": latest.get("progress"),
            "url": latest.get("url"),
            "seconds": latest.get("seconds"),
            "size": latest.get("size"),
            "payload": latest,
            "poll_url": f"/api/agnes/video/status?task_id={video_id or task_id}",
        }
    )


@app.route("/api/agnes/video/status", methods=["GET"])
def agnes_video_status():
    task_id = request.args.get("task_id") or request.args.get("video_id") or ""
    if not task_id:
        return jsonify({"error": "缺少 task_id 或 video_id"}), 400

    api_key = (request.args.get("api_key") or AGNES_API_KEY).strip()
    result_payload = query_video_status(api_key, task_id)
    return jsonify(
        {
            "task_id": result_payload.get("id") or result_payload.get("task_id") or task_id,
            "video_id": result_payload.get("video_id") or task_id,
            "status": result_payload.get("status"),
            "progress": result_payload.get("progress"),
            "url": result_payload.get("url"),
            "seconds": result_payload.get("seconds"),
            "size": result_payload.get("size"),
            "payload": result_payload,
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    threading.Timer(1.0, lambda: open_browser(f"http://127.0.0.1:{port}")).start()
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
