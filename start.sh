#!/bin/bash
cd /home/sumit-x/Downloads/google-maps-scraper-kit-master
source venv/bin/activate
sudo docker compose up -d > /dev/null 2>&1
if ! pgrep -f "streamlit run app.py --server.port 8502" > /dev/null; then
    nohup streamlit run app.py --server.port 8502 > /dev/null 2>&1 &
    sleep 3
fi
xdg-open http://localhost:8502
