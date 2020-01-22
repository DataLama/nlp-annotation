#### doccano install ####
mkdir annotation

# doccano 프로젝트 가져오기
git clone https://github.com/chakki-works/doccano.git

# docker image pull
docker pull chakkiworks/doccano  

# python 환경 구축
brew install postgresql
pip install -r requirements.txt # sudo apt install requirements.txt

cd app/server/static
brew install npm # 안되면 기존 ver 삭제하고 재설치 sudo apt install npm
npm install cross-env
npm install --dev
npm run build

# run docker image
docker-compose pull

nvidia-docker run -itd -v nlp_dataset:/data -d -it --name doccano -p 8000:8000 chakkiworks/doccano

docker exec -it doccano tools/create-admin.sh "admin" "sujinkim23@amorepacific.com" "amore12345"

# web ui url: http://10.160.210.118:8000/login/ 
# id: admin, pw: amore12345

# GPU 서버에 install 시 에러 나면 
npm cache clean --force
rm -rf node_modules
npm install
