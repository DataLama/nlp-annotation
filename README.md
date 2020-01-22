# nlp-annotation
- 웹 기반의 nlp tagging platform doccano 설치 및 운영.
- Document Classification, Named entity recognition, Seq2Seq를 위한 데이터 라벨링 가능.

## doccano
doccano is an open source text annotation tool for human. It provides annotation features for text classification, sequence labeling and sequence to sequence. So, you can create labeled data for sentiment analysis, named entity recognition, text summarization and so on. Just create project, upload data and start annotation. You can build dataset in hours.

[https://github.com/chakki-works/doccano](https://github.com/chakki-works/doccano)

## Doccano 설치.
> WARNING 19.08월의 기록임. 설치 에러 발생가능. 위 git에서 변경 사항 확인 요함.
> 본 설치 방법은 `docker compose`가 아닌 `docker run`으로 실행함. 제대로 구축하려면 `docker compose`로 해라.

### 1) Run Your Container
```bash
    docker run -itd -v nlp_dataset:/data --name {CONTAINER NAME} -p {DOCCANO_PORT}:8000 -p {JUPYTER_PORT}:8888 annotation_ap_1:latest
```
- `{CONTAINER NAME}` 컨테이너 이름. 뒤에 담당자 아이디.
- `{DOCCANO_PORT}` doccano 웹 port 번호.
- (OPTIONAL) `{JUPYTER_PORT}` jupyter 띄우고 싶으면 사용. 웬만해서는 그냥 쓰는게 좋을 듯!

### 2) Creating SuperUser
```bash
    docker exec {CONTAINER NAME} tools/create-admin.sh {"담당자 ID"} {"mail-id@mail-domain.com"} {"password"}
```

### 3) Set the DB of Doccano
- single container로 doccano를 실행할 경우 sqlite DB사용. => pandas로 관리하는게 편함.
- docker compose로 doccano를 실행할 경우 postgresql 사용. => DBMS로 관리하는게 좋을 듯.

#### Create the project 
- 먼저 웹을 통해서 프로젝트를 생성해두자. 프로젝트 번호는 1부터 시작하며, 새로운 프로젝트를 생성할 때마다 1씩 증가함.

#### RUN `label_setup.py`
- 일부 클래스만 업로드 할 경우 파라미터를 `voc_class`가 아닌 `sub_class`로 변경.

#### RUN `document_setup.py`
- 데이터 파일 또는 프로젝트가 바뀔 경우 변수 변경.

### 4) Aggregate the data
- `agg.py`로 데이터들을 취합해서 csv로 떨구자.


## Installation Issue

### clone the repository
```bash
    git clone <https://github.com/chakki-works/doccano.git>
    cd doccano
```
### change the Dockerfile and build

- 원래 dockerfile의 경우 user가 root가 아니어서 새로운 패키지를 설치하지 못함.
```dockerfile
    USER doccano 
    WORKDIR /doccano
    EXPOSE ${PORT}
```
- `USER doccano`를 제거하면 자동으로 root권한으로 container를 관리할 수 있음.
- `docker build --tag=annotation .`을 통해 docker **이미지 생성**.

> 설치 에러 발생 시, `annotation_install.sh`코드 참조.

### Set up
```bash
    apt update
    apt install vim -y && apt install graphviz -y && apt install libgraphviz-dev -y
    pip install jupyterlab pandas sqlalchemy eralchemy xlrd matplotlib
```

## 필요 개선사항
### docker compose up을 활용한 단일 웹서버 생성과 super-user를 통한 user 및 데이터 관리 방법 찾기.