Запуск:

```
git clone https://github.com/boysmail/yaprofi-prog2023
cd yaprofi-prog2023
pip install -r requirements.txt
python app.py
```

Можно запустить docker container: 
```
git clone https://github.com/boysmail/yaprofi-prog2023
cd yaprofi-prog2023
docker build -t yaprofi-prog2023 .
docker run -p 8080:8080 yaprofi-prog2023
```
После этого api будет доступен на `127.0.0.1`