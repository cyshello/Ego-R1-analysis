import requests
import json
import os
from utils import constants

def test_video_llm_api(question, video_range, identity=None, vid_id=None):
    """
    Test the video_llm API.
    Expected payload is a list of objects.
    """
    url = constants.VIDEO_LLM_URL
    
    payload = {
        "question": question,
        "range": video_range
    }
    
    if identity:
        # The API usually expects just the prefix (e.g., 'A1' from 'A1_JAKE')
        payload["identity"] = identity.split('_')[0]
    elif vid_id:
        payload["vid_id"] = vid_id
    else:
        print("Error: Either identity or vid_id must be provided.")
        return

    try:
        print(f"\n[Video LLM] Sending payload to {url}:")
        print(json.dumps([payload], indent=2))
        
        # Note: video_llm expects a LIST of payloads
        response = requests.post(url, json=[payload], timeout=420)
        response.raise_for_status()
        
        results = response.json()
        print("Response:", json.dumps(results, indent=2))
        return results
    except Exception as e:
        print(f"Video LLM API error: {e}")

def test_vlm_api(question, timestamp, identity=None, vid_id=None):
    """
    Test the vlm API.
    Expected payload is a single object.
    """
    url = constants.VLM_URL
    
    payload = {
        "question": question,
        "timestamp": timestamp
    }
    
    if identity:
        payload["identity"] = identity.split('_')[0]
    elif vid_id:
        payload["vid_id"] = vid_id
    else:
        print("Error: Either identity or vid_id must be provided.")
        return

    try:
        print(f"\n[VLM] Sending payload to {url}:")
        print(json.dumps(payload, indent=2))
        
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        results = response.json()
        print("Response:", json.dumps(results, indent=2))
        return results
    except Exception as e:
        print(f"VLM API error: {e}")

if __name__ == "__main__":
    # --- Video LLM Test ---
    print("--- Testing Video LLM ---")
    test_video_llm_api(
        question="What is the person doing in the kitchen?",
        video_range=[0, 30], # seconds
        identity="A1_JAKE"
    )

    # --- VLM Test ---
    print("\n--- Testing VLM ---")
    test_vlm_api(
        question="What is on the table?",
        timestamp=15, # second
        identity="A1_JAKE"
    )
