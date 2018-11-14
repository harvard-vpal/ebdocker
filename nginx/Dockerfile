# Dockerfile for bridge nginx

# Base app image, tag to use
ARG APP_IMAGE

# Collect static resources with base image
FROM ${APP_IMAGE} as app
RUN python manage.py collectstatic -c --noinput --settings=config.settings.eb.nginx

# Copy static resources from base stage to nginx image
FROM nginx
RUN mkdir -p /www/static
COPY --from=app /www/static /www/static
RUN rm /etc/nginx/conf.d/default.conf
ADD sites-enabled/ /etc/nginx/conf.d
