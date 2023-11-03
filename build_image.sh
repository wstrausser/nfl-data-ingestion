name=schedule-ingestion-prod

docker build -t wstrausser/$name:latest .

docker push wstrausser/$name:latest