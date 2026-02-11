import requests
import json
# constants.py에 정의된 URL을 사용하거나 직접 문자열로 입력하세요.
from utils import constants 

def test_rag_api(identity, level, keywords, start_time, query_time, vid_id=None):
    # 1. 페이로드 설정
    payload = {
        "level": level,
        "keywords": keywords,
        "start_time": start_time,
        "query_time": query_time,
    }
    
    # 2. 특정 identity가 아닐 경우 vid_id 추가 (코드 로직 반영)
    if identity not in ["A1_JAKE", "A2_ALICE", "A3_TASHA", "A4_LUCIA", "A5_KATRINA", "A6_SHURE"]:
        if vid_id:
            payload['vid_id'] = vid_id

    # 3. URL 설정 (constants.py의 RAG_URL 딕셔너리 참조)
    url = constants.RAG_URL.get(identity)
    
    if not url:
        print(f"Error: No URL found for identity {identity}")
        return

    try:
        # 4. API 요청
        print(f"Sending payload to {url}: {json.dumps(payload, indent=2)}")
        response = requests.post(url, json=payload)
        response.raise_for_status() # 에러 발생 시 예외 처리
        
        results = response.json()
        print("Response:", json.dumps(results, indent=2))
        return results
    except Exception as e:
        print(f"Tool call error: {e}")

# --- 실행 예시 ---
if __name__ == "__main__":
    test_rag_api(
        identity="A1_JAKE", 
        level="hour",
        keywords=["pick up marker"], 
        start_time="DAY1_11000000", 
        query_time="DAY1_11350000"
    )