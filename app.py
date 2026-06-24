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
        # فك الاختصار برمجياً لو الرابط جاي من vt.tiktok
        if "vt.tiktok.com" in tiktok_url:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.head(tiktok_url, headers=headers, allow_redirects=True)
            tiktok_url = res.url

        # إرسال الرابط النهائي المستقر مباشرة إلى الـ API الخارجي الشغال
        api_url = f"https://www.tikwm.com/api/?url={tiktok_url}"
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            video_url = response["data"]["play"]
            return jsonify({
                "status": "success",
                "video_url": video_url
            })
        else:
            return jsonify({"status": "error", "message": "Failed to parse video from tikwm API"}), 400
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
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
