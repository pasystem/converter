FROM python:3.9-alpine

RUN apk add --update --no-cache libgcc libstdc++ libx11 glib libxrender libxext libintl  \
    ttf-dejavu ttf-droid ttf-freefont ttf-liberation msttcorefonts-installer \
    && update-ms-fonts \
    && fc-cache -f

# On alpine static compiled patched qt headless wkhtmltopdf (46.8 MB).
# Compilation took place in Travis CI with auto push to Docker Hub see
# BUILD_LOG env. Checksum is printed in line 13685.
COPY --from=madnight/alpine-wkhtmltopdf-builder:0.12.5-alpine3.10 /bin/wkhtmltopdf /usr/bin/wkhtmltopdf
COPY app/ /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--workers", "4"]
