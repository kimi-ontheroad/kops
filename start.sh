nginx -t
nginx -c /etc/nginx/nginx.conf
nginx -s reload
cd backend
rm -rf celerybeat.pid celerybeat-schedule.db
nohup redis-server > log/redis.log 2>&1 &
nohup celery -A backend  beat -l info > log/beat.log 2>&1 &
nohup celery -A backend worker -l info > log/worker.log 2>&1 &
# 每隔5秒使用nc 检查端口 mysql 3306是否通
while ! nc -z db 3306;
do
echo "wait for mysql database init start";
sleep 5;
done;
echo "mysql database is ready!"
python3 /code/backend/manage.py runserver 127.0.0.1:8000
