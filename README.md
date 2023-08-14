# binscot-api
# 

패키지 저장 : pip freeze > requirements.txt
패키지 install :pip install -r requirements.txt



# docker

이미지생성
docker build -t [repo]/[tag]:latest . 

push

docker push  [repo]/[tag]:latest  

pull

sudo docker pull [repo]/[tag]

run

sudo docker run -p 80:80 [repo]/[tag]

상태확인
sudo docker ps

종료
sudo docker stop [port]
