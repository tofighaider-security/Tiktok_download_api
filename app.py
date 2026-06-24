import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_video', methods=['GET'])
def get_video():
    tiktok_url = request.args.get('url')
    
    if not tiktok_url:
        return jsonify({"status": "error", "message": "Missing url parameter"}), 400
        
    try:
        # إذا كان الرابط مختصراً، نقوم بتتبعه للحصول على الرابط الأصلي الكامل
        if "vt.tiktok.com" in tiktok_url or "v.douyin.com" in tiktok_url:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.head(tiktok_url, headers=headers, allow_redirects=True)
            tiktok_url = res.url

        # إرسال الرابط النهائي إلى الـ API الخارجي
        api_url = f"https://www.tikwm.com/api/?url={tiktok_url}"
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            video_url = response["data"]["play"]
            return jsonify({
                "status": "success",
                "video_url": video_url
            })
        else:
            return jsonify({"status": "error", "message": "Failed to parse video from API"}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

