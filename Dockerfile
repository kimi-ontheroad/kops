FROM neverqaz/ubuntu:python_nginx_vue
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD ./ /code/
WORKDIR /code
RUN  apt install expect -y \
&& pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r backend/requirements.txt  --default-timeout=100 \
&& apt install redis-server -y \
&& cd front \
&& npm install -g vue-cli \
&& npm install --save vue-cookie \
&& npm install \
&& npm run build \
&& mv /code/nginx.conf /etc/nginx/conf.d/
CMD ["/bin/bash", "start.sh"]
EXPOSE 8000 8080



