name=prod-nfl-data-ingestion

docker build -t wstrausser/$name:latest .

docker push wstrausser/$name:latest