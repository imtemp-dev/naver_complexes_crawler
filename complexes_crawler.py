import os
import json
import requests
from pathlib import Path

# API 요청에 필요한 쿠키와 헤더 설정
cookies = {
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.trade_type_cd': '""',
    'nhn.realestate.article.ipaddress_city': '1100000000',
    '_fwb': '1228ESXyx0yhUfRFcmxcDZB.1748138823864',
    'landHomeFlashUseYn': 'Y',
    'NNB': 'YUJNZU2IPMZGQ',
    'NAC': '7jtSBogQfGUrA',
    'NACT': '1',
    'REALESTATE': 'Sun%20May%2025%202025%2011%3A07%3A09%20GMT%2B0900%20(Korean%20Standard%20Time)',
    '_fwb': '1228ESXyx0yhUfRFcmxcDZB.1748138823864',
    'BUC': 'u6aapYZkoMo9_rem15b2ieSEhW77iCjbxS1tiHTmD8g=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDgxMzg4MjksImV4cCI6MTc0ODE0OTYyOX0.w2_WPgP306m4Hcpo9b97JRRS07A1YjebOw8m-a6ojPU',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://new.land.naver.com/complexes?ms=37.3595704,127.105399,16&a=APT:ABYG:JGC:PRE&e=RETAIL',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

def load_region_data(file_path):
    """지역 데이터 파일을 로드합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_directory_structure(region_data):
    """지역 데이터를 기반으로 디렉토리 구조를 생성합니다."""
    # complexes 폴더 생성
    base_dir = Path('complexes')
    base_dir.mkdir(exist_ok=True)
    
    # 시 단위 정보 가져오기
    cities = region_data['current']['regionList']
    
    for city in cities:
        city_name = city['cortarName']
        city_code = city['cortarNo']
        
        # 시 폴더 생성
        city_dir = base_dir / city_name
        city_dir.mkdir(exist_ok=True)
        
        # 해당 시의 구 정보가 있는지 확인
        if city_code in region_data['children']:
            districts = region_data['children'][city_code]['current']['regionList']
            
            for district in districts:
                district_name = district['cortarName']
                district_code = district['cortarNo']
                
                # 구 폴더 생성
                district_dir = city_dir / district_name
                district_dir.mkdir(exist_ok=True)
                
                # 해당 구의 동 정보가 있는지 확인
                if district_code in region_data['children'][city_code]['children']:
                    dongs = region_data['children'][city_code]['children'][district_code]['current']['regionList']
                    
                    for dong in dongs:
                        dong_name = dong['cortarName']
                        cortarNo = dong['cortarNo']
                        
                        # 동별 단지 정보 가져오기
                        complexes = fetch_complexes(cortarNo)
                        
                        if complexes:
                            # 동별 단지 정보 저장
                            filename = f"{dong_name}_complexes.json"
                            save_complexes(district_dir / filename, complexes)
                            print(f"{city_name}/{district_name}/{filename} 저장 완료")

def fetch_complexes(cortarNo):
    """특정 지역의 단지 정보를 가져옵니다."""
    params = {
        'cortarNo': cortarNo,
        'realEstateType': 'APT:ABYG:JGC:PRE',
        'order': '',
    }
    
    try:
        response = requests.get(
            'https://new.land.naver.com/api/regions/complexes', 
            params=params, 
            cookies=cookies, 
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API 요청 실패: {response.status_code} - {cortarNo}")
            return None
    except Exception as e:
        print(f"API 요청 중 오류 발생: {e} - {cortarNo}")
        return None

def save_complexes(file_path, data):
    """단지 정보를 JSON 파일로 저장합니다."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 지역 데이터 파일 경로
    region_data_file = "region_data_20250525_143203.json"
    
    # 지역 데이터 로드
    region_data = load_region_data(region_data_file)
    
    # 디렉토리 구조 생성 및 데이터 수집
    create_directory_structure(region_data)
    
    print("모든 단지 정보 수집 완료") 