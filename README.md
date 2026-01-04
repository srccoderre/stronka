# 💰 Skarbiec VIP - System Zarządzania Portfelem Finansowym

Enterprise-grade aplikacja do zarządzania finansami osobistymi, inwestycjami i śledzenia celów finansowych.

## 🎯 Główne Funkcjonalności

- ✅ Śledzenie dochodów & wydatków
- ✅ Zarządzanie inwestycjami (złoto, srebro, akcje, kryptowaluty, obligacje, ETF)
- ✅ Ustawienie celów finansowych
- ✅ Zaawansowana analityka
- ✅ Powiadomienia real-time
- ✅ PWA - aplikacja offline

## 🏗️ Technologia

- Python 3.12 + FastAPI
- PostgreSQL 16
- Redis 7
- Vanilla JavaScript
- Docker

## 🚀 Szybki Start
```bash
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec api alembic upgrade head
```

## 📊 Dostęp

- Frontend: https://skarbiec.vip
- API: https://skarbiec.vip/docs
- Grafana: http://146.19.213.161:3000
- Flower: http://146.19.213.161:5555
- PgAdmin: http://146.19.213.161:5050

## 📄 Licencja

MIT
