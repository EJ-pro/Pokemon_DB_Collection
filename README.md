# 📑 Pokemon_DB_Collection

> **LLM 및 RAG 시스템 구축을 위한 하이브리드 포켓몬 데이터 수집 엔진**

이 프로젝트는 포켓몬 관련 정형 데이터(API)와 비정형 데이터(Web)를 체계적으로 수집하여, 차세대 질의응답 시스템의 기반이 되는 지식 베이스를 구축하는 것을 목표로 합니다.

---

## 🎯 수집 전략 (Collection Strategy)

데이터의 신뢰성과 맥락의 풍부함을 동시에 잡기 위해 **3단계 하이브리드 수집 전략**을 채택합니다.

### Phase 1. 정형 데이터 수집 (PokeAPI 기반)
* **목적:** 수치 데이터의 무결성 확보 (할루시네이션 방지용 Fact 데이터)
* **대상:** 종족값, 타입 상성, 진화 트리, 기술(Move) 정보
* **방식:** REST API를 통한 JSON 데이터 파싱 및 RDBMS 저장

### Phase 2. 비정형 데이터 수집 (Web Scraping 기반)
* **목적:** LLM의 풍부한 답변 생성을 위한 맥락 정보 확보
* **대상:** 포켓몬 위키(Lore), 나무위키(배틀 팁, 유저 평가), 공식 도감 설명
* **방식:** BeautifulSoup/Scrapy를 활용한 텍스트 추출 및 정규화

### Phase 3. RAG 최적화 전처리 (Processing)
* **목적:** 벡터 검색 및 SQL 연동 효율화
* **내용:** 데이터 청킹(Chunking), 메타데이터 매핑, 임베딩(Embedding) 생성

---

## 📊 수집 대상 데이터 상세 (Data Scope)

| 카테고리 | 상세 데이터 항목 | 출처 | 활용 방안 |
| :--- | :--- | :--- | :--- |
| **기본 정보** | 이름, 도감 번호, 세대, 신장, 무게 | PokeAPI | 기본 정보 조회 |
| **능력치** | HP, 공격, 방어, 특공, 특방, 스피드 | PokeAPI | Text-to-SQL 분석 |
| **관계성** | 진화 단계, 진화 조건, 타입 상성 | PokeAPI | 복잡한 논리 쿼리 |
| **설정/도감** | 세대별 도감 설명, 배경 스토리 | Wiki/Web | 의미 기반 벡터 검색 |
| **실전 데이터** | 추천 성격, 도구, 기술 배치, 샘플 | 커뮤니티 | 배틀 코칭 서비스 |

---

## 🛠 기술 스택 (Tech Stack)

* **Language:** Python 3.9+
* **Data Collection:** `Requests` (API), `BeautifulSoup4` / `Playwright` (Scraping)
* **Database:** * **PostgreSQL:** 정형 데이터 관리 및 관계 정의
    * **pgvector:** 텍스트 임베딩 데이터 저장 (Vector DB)
* **Processing:** `Pandas` (ETL), `LangChain` (Text Splitter)

---

## 🗂 프로젝트 구조 (Directory Structure)

```text
Pokemon_DB_Collection/
├── collectors/           # 데이터 수집 스크립트
│   ├── api_collector.py  # PokeAPI 호출 로직
│   └── web_scraper.py    # 위키 크롤링 로직
├── data/                 # 수집된 Raw 데이터 (JSON/CSV)
├── database/             # DB 스키마 및 마이그레이션
│   ├── schema.sql        # ERD 기반 테이블 설계
│   └── vector_store.py   # 벡터 저장소 연동
├── processing/           # 데이터 정제 및 임베딩 로직
└── README.md
```