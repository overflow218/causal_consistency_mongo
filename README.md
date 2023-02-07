# causal_consistency_mongo

#### YCSB 활용

1. https://github.com/brianfrankcooper/YCSB 에서 다운로드. 최신버전 체크하기
2. 디비별로 디렉토리에 있는 README 확인

#### YCSB for mongodb

1. JAVA, Maven 설치
2. MongoDb 설치
3. ./bin/ycsb.sh 파일을 실행. (공식 깃헙 문서는 ./bin/ycsb 로 나와있는데 이렇게 하면 실행안됨)

- ex) ./bin/ycsb.sh [load/run] [dbname] [각종 옵션]

4. [옵션 정리]
   -threads = ycsb 클라이언트 쓰레드 개수, 기본 1개
   -target = 초당 목표 opertaion 개수, 이걸 늘리면 latency가 늘어남.
   -s = status 옵션. 이걸 걸어주면 실행중에 10초마다 status report 찍어줌. 넣는게 좋음
   -P = 대문자 P. load property files를 지정할때 사용. 보통 workloads/워크로드파일 만들어져있는 요거 씀. 만들어져 있는 파일에서 비율을 조절하거나 맘에 안들면 형식에 맞춰서 새로 만들면 됨.
   -p = 소문자 p. 사용하는 디비에 맞게 각종 parameter를 넘겨줄때 사용
   -p로 넘겨줄 수 있는 주요 properties
   - recordcount = 워크로드 시작할때 존재하는 데이터 레코드 개수. 기본 1000
   - operationcount = 워크로드동안 실행되는 operation 횟수. 기본 1000
   - threadcount = 쓰레드 개수. 위에 -threads와 동일한 기능
   - db = database class to use. Alternatively this may be specified on the command line. (default: com.yahoo.ycsb.BasicDB)
   - 기타 더 자세한 인자들은 https://github.com/brianfrankcooper/YCSB/wiki/Core-Properties 참고
5. 실제 예시 명령
   ./bin/ycsb.sh load mongodb -s -P workloads/workloada -p recordcount=1000 -threads 2 -p mongodb.url="mongodb://mongo:mongo@localhost:27107/?w=majority&replicaSet=rs0&readPreference=secondary" -p mongodb.auth="true"

   - 해석: 몽고디비 쓸꺼고, workloada 를 활용할거임. 레코드 개수는 천개, 쓰레드 2개, 로컬호스트 27018포트에 있는 몽고디비에 접속할거임.
   - 레플리카셋이나 WR concern 관련 정보는 url에 포함해서 넣으면 됨
   - authentication이 필요한경우 위와 같이 username:password@주소 형식으로 넣어주고 auth = 'true'를 넣어줘야함.

   ./bin/ycsb.sh run mongodb -s -P workloads/workloada -p operationcount=1000 -threads 2 -p mongodb.url="mongodb://mongo:mongo@localhost:27017" -p mongodb.auth="true" > workloadc_test.result

   - 해석: 몽고디비로 workloada실행할거임. 연산횟수는 1000번 쓰레드는 2개 쓸거임. 결과를 worklaodc_test.result 파일에 저장할거임.

#### Core Workloads

공식문서 https://github.com/brianfrankcooper/YCSB/wiki/Core-Workloads

- Workload A: Update heavy workload : 데이터의 50%를 db에서 읽고 50%를 db에 쓴다.
  Application example: Session store recording recent actions
  Read/update ratio: 50/50
  Request distribution: zipfian

- Workload B: Read mostly workload : 데이터의 95%를 db에서 읽고 5%를 db에 쓴다.
  Application example: photo tagging; add a tag is an update, but most operations are to read tags
  Read/update ratio: 95/5
  Request distribution: zipfian

- Workload C: Read only : 데이터의 100%를 db에서 읽는다.
  Application example: user profile cache, where profiles are constructed elsewhere (e.g., Hadoop)
  Read/update ratio: 100/0
  Request distribution: zipfian

- Workload D: Read latest workload : 새로운 데이터를 db에 저장하고, 가장 최근에 저장된 데이터들을 읽는다.
  Application example: user status updates; people want to read the latest
  Read/update/insert ratio: 95/0/5
  Request distribution: latest

- Workload E: Short ranges : 각각의 데이터를 쿼리하는 대신, 어떤 좁은(혹은 짧은) 구간 내에 속하는 데이터들을 쿼리한다.

  Application example: threaded conversations, where each scan is for the posts in a given thread (assumed to be clustered by thread id)
  Scan/insert ratio: 95/5
  Request distribution: zipfian

- Workload F: Read-modify-write : 데이터를 읽고, 수정한 후, 그 수정된 데이터를 다시 db에 쓴다
  Application example: user database, where user records are read and modified by the user or to record user activity.
  Read/read-modify-write ratio: 50/50
  Request distribution: zipfian

##### 공식문서 추천 실행순서

1. Load the database, using workload A’s parameter file (workloads/workloada) and the “-load” switch to the client.
2. Run workload A (using workloads/workloada and “-t”) for a variety of throughputs.
3. Run workload B (using workloads/workloadb and “-t”) for a variety of throughputs.
4. Run workload C (using workloads/workloadc and “-t”) for a variety of throughputs.
5. Run workload F (using workloads/workloadf and “-t”) for a variety of throughputs.
6. Run workload D (using workloads/workloadd and “-t”) for a variety of throughputs. This workload inserts records, increasing the size of the database.
7. Delete the data in the database.
8. Reload the database, using workload E’s parameter file (workloads/workloade) and the "-load switch to the client.
9. Run workload E (using workloads/workloade and “-t”) for a variety of throughputs. This workload inserts records, increasing the size of the database.

요약: 워크로드별로 데이터셋 거의 비슷하니까 workloada 올려서 데이터베이스 사이즈 안바뀌는 a, b, c, f, d 워크로드 확인 -> 테이블 버리고 다시 로드 -> e 워크로드 확인
