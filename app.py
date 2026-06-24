import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_video', methods=['GET'])
def get_video():
    tiktok_url = request.args.get('url')
    
    if not tiktok_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        # استخدام واجهة ذكية ومستقرة لاستخراج الفيديو
        api_url = f"https://www.tikwm.com/api/?url={tiktok_url}"
        response = requests.get(api_url).json()

        if response.get("code") == 0:
            video_url = response["data"]["play"]
            return jsonify({
                "status": "success",
                "video_url": video_url
            })
        else:
            return jsonify({"status": "error", "message": "Failed to parse video"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# مسحنا أسطر app.run والـ port تماماً لأن Vercel لا تحتاجها.
