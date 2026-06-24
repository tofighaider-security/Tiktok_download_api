import os
from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def clean_tiktok_url(url):
    # إذا كان الرابط مختصراً، نقوم بفك الاختصار برمجياً
    if "vt.tiktok.com" in url or "v.douyin.com" in url:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.head(url, headers=headers, allow_redirects=True)
        url = res.url
    return url

@app.route('/get_video', methods=['GET'])
def get_video():
    tiktok_url = request.args.get('url')
    
    if not tiktok_url:
        return jsonify({"status": "error", "message": "Missing url parameter"}), 400
        
    try:
        full_url = clean_tiktok_url(tiktok_url)
        
        # استخراج المعرف الفريد للفيديو باستخدام الـ Regex لضمان الدقة
        video_id_match = re.search(r'/video/(\d+)', full_url)
        if not video_id_match:
            return jsonify({"status": "error", "message": "Invalid TikTok URL structure"}), 400
            
        video_id = video_id_match.group(1)
        
        # استخدام واجهة بديلة ومستقرة ومباشرة لجلب بيانات الفيديو بدون علامة مائية
        api_url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
        }
        
        response = requests.get(api_url, headers=headers).json()
        
        # استخراج رابط الفيديو المباشر بدون العلامة المائية
        aweme_list = response.get("aweme_list", [])
        if aweme_list:
            video_data = aweme_list[0].get("video", {})
            # روابط play_addr تحتوي عادةً على الفيديو النظيف
            download_url = video_data.get("play_addr", {}).get("url_list", [None])[0]
            
            if download_url:
                return jsonify({
                    "status": "success",
                    "video_url": download_url
                })
                
        return jsonify({"status": "error", "message": "Unable to extract video stream"}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
