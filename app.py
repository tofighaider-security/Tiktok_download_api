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
        # فك الاختصار برمجياً بنجاح وديناميكية
        if "vt.tiktok.com" in tiktok_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            res = requests.head(tiktok_url, headers=headers, allow_redirects=True)
            tiktok_url = res.url

        # إرسال الرابط الصافي للـ API الخارجي الشغال
        api_url = f"https://www.tikwm.com/api/?url={tiktok_url}"
        req_res = requests.get(api_url)
        
        # التأكد من أن الرد نصي وليس فارغاً لتجنب خطأ تشريح الـ JSON
        try:
            response = req_res.json()
        except Exception:
            return jsonify({"status": "error", "message": "External API returned non-JSON response", "raw": req_res.text[:200]}), 502
        
        if response.get("code") == 0:
            video_url = response["data"]["play"]
            return jsonify({
                "status": "success",
                "video_url": video_url
            })
        else:
            return jsonify({"status": "error", "message": response.get("msg", "Failed to parse video from tikwm API")}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
