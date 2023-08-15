# binscot-api
# 

패키지 저장 : pip freeze > requirements.txt
패키지 install :pip install -r requirements.txt

## oracle

무료 arm 서버

api, db 
 ocpu : 3
 메모리 : 18GB

fornt
 ocpu : 1
 메모리 : 6GB

오라클 무료 서버는 총 4개의 ocpu 24GB 의 메모리 200GB 의 용량  2개의 VCN

백엔드 서버와 프론트서버 DB 서버를 나누고싶었으나
VCN 을 2개밖에 생성불가
백엔드서버(fastApi), DB(postgresql) 를 하나에 서버에 배치
-> 백엔드와 DB 간의 통신이 동일한 서버에서 이루어지므로 네트워크 레이턴시가 감소 이로 인해 데이터 요청 및 응답 시간이 단축 예상

프론트서버 Next.js 13 구성예정
 
## docker

이미지생성
docker build -t [repo]/[tag]:latest . -f DockerFile   

push

docker push  [repo]/[tag]:latest 

pull

sudo docker pull [repo]/[tag]

run

sudo docker run -p 80:80 -e TZ=Asia/Seoul [repo]/[tag]

상태확인
sudo docker ps

종료
sudo docker stop [port]

docker 접속 docker exec -it [container] /bin/bash
