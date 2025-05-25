# 네이버 부동산 단지 정보 크롤러

네이버 부동산에서 시/구/동 계층 구조에 따른 단지 정보를 수집하는 프로그램입니다.

## 기능

- 시/구/동 계층 구조로 폴더 생성
- 각 동별 단지 정보를 JSON 파일로 저장
- 네이버 부동산 API를 통한 실시간 데이터 수집

## 사용 방법

1. Poetry 환경 설치:
```bash
poetry install
```

2. 프로그램 실행:
```bash
poetry run python complexes_crawler.py
``` 