"""
마지막 업데이트 : 2017-09-13
파일명 : readme.txt

실행소스 및 데이터 path 정보이다.
class 나 재사용성을 크게 고려하지 않는 소스들이다. 반복되는 것이 많고, 물흐르듯이 실행되므로 소스파악은 쉽다.
그러나 반복되는게 너무 많아지고 힘들다고 판단되면 class를 만드는 것을 추천한다.

참고로 windows7 32bit에 설치된 몽고 실행은 cmd 에서
mongod --storageEngine=mmapv1 하면되고,
접속은 mongo 치면 된다.

cmd 상에서 직접 py를 실행할 거라면
내컴퓨터 환경변수에 PYTHONPATH dw경로(예=> D:\srkim\python\project\dw\dw)를 추가해준다.
"""
dw
├─data => 원본 데이터 관리
│  └─fred
│      ├─init => 최초
│      │  ├─category
│      │  │      10.json => cate id 별 series 리스트
│      │  │      ...
│      │  │
│      │  ├─ids
│      │  │      categories.csv         => cate id list
│      │  │      categories_product.csv => 사용자 정의 cate id list
│      │  │      categories.json        => 모든 cate id 의 부모자식 관계 및 메타 정보를 하나의 json으로
│      │  │      series.csv             => series id list
│      │  │
│      │  └─series
│      │      │  ACILOB.json            => series meta
│      │      │  ...
│      │      │
│      │      └─observ
│      │              ACILOB.json       => 해당 series의 observation
│      │              ...
│      │
│      └─update => 업데이트
│          │  last_update_start_time.txt
│          │
│          └─series
│              │  R2500VLTR.json
│              │  ...
│              │
│              └─observ
│                      R2500VLTR.json
│                      ...
│
├─dw => 소스코드 관리
│  │
│  ├─common
│  │     config.py => 모든 agency가 공통적으로 쓰는 설정 정보
│  │     util.py   => 모든 agency가 공통적으로 쓰는 util
│  │  
│  └─fred
│       01_init_category.py            => category 데이터 생성
│       02_init_seriess_thread.py      => category 별 seriess list 데이터 생성
│       03_init_seriess_meta_thread.py => seires meta 생성
│       04_init_observ_thread.py       => observation 생성
│       05_update.py                   => fred api update 목록을 가져와서 series meta / observation 갱신
│       06_parse_init.py               => init 데이터 파싱
│       07_parse_update.py             => update 데이터 파싱
│       08_db_init.py                  => db init
│       09_db_update.py                => db update
│       api.py                         => python fred api 라이브러리
│       readme.txt                     => 소스 정보
│       path.py                        => url / file path 관련 정보
│       util.py                        => fred의 util
│  
└─parsed => parsed 데이터 관리, data 폴더 구조를 그대로 활용
    └─fred
        ├─init
        │  └─series
        │      │  ACILOB.json
        │      │  ...
        │      │
        │      └─observ
        │              ACILOB.json
        │              ...
        │
        └─update
           └─series
               │  R2500VLTR.json
               │  ...
               │
               └─observ
                       R2500VLTR.json
                       ...
