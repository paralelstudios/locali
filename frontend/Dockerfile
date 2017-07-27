FROM nginx

# Install Node.js and other dependencies
RUN apt-get update && \
    apt-get -y install curl gnupg && \
    curl -sL https://deb.nodesource.com/setup_4.x | bash - && \
    apt-get -y install build-essential nodejs

COPY ./frontend-nginx.conf /etc/nginx/nginx.conf
COPY . /usr/src/app
WORKDIR /usr/src/app

RUN npm install
RUN npm run build

RUN cp index.html base.css /usr/share/nginx/html
RUN cp -r dist/ /usr/share/nginx/html/dist
RUN cp -r resources/ /usr/share/nginx/html/resources
