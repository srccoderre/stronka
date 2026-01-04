# 💰 Mój Portfel 2026

Enterprise-grade Financial Management System - Complete full-stack application for personal finance tracking and investment management.

## 🚀 Features

### Core Functionality
- **JWT Authentication** - Secure access and refresh token system
- **Daily Financial Entries** - Track income, expenses with categories
- **Investment Management** - Gold, silver, stocks, crypto, ETF, bonds, real estate
- **Monthly/Yearly Goals** - Set and track financial objectives
- **Advanced Analytics** - Dashboard, trends, forecasts, category breakdowns
- **In-app Notifications** - Real-time updates and alerts
- **Background Tasks** - Email, reports, data cleanup via Celery
- **PWA Support** - Offline functionality, installable app

### Technical Features
- **Async/Await** throughout the stack
- **Custom Exception Handling** with proper error responses
- **Rate Limiting** (5 req/min for auth endpoints)
- **Structured Logging** with structlog
- **Soft Delete** for user data
- **Redis Caching** for frequently accessed data
- **JWT Token Rotation** for enhanced security
- **Argon2/BCrypt** password hashing
- **Input Validation** with Pydantic 2.5+

## 🏗️ Tech Stack

### Backend
- **Python 3.12**
- **FastAPI 0.109+** - Modern async web framework
- **SQLAlchemy 2.0+** - Async ORM with asyncpg
- **PostgreSQL 16** - Primary database
- **Redis 7** - Caching and session storage
- **Celery 5.3+** - Background task processing
- **Pydantic 2.5+** - Data validation
- **Alembic** - Database migrations
- **python-jose** - JWT handling
- **passlib** - Password hashing
- **structlog** - Structured logging

### Frontend
- **Vanilla JavaScript (ES6+)** - No framework dependencies
- **Chart.js** - Data visualization
- **PWA** - Service Worker for offline support
- **IndexedDB** - Client-side storage
- **Responsive CSS** - Mobile-first design

### Infrastructure
- **Docker & Docker Compose**
- **Nginx** - Reverse proxy and static file serving
- **Prometheus** - Metrics collection
- **Grafana** - Monitoring dashboards
- **Loki** - Log aggregation
- **Promtail** - Log shipping
- **PgAdmin** - Database administration
- **Flower** - Celery monitoring

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)
- Node.js (optional, for frontend tooling)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/srccoderre/protmonetlka.git
cd protmonetlka
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services
```bash
# Development
make up

# Production
make prod-up
```

### 4. Run Migrations
```bash
make migrate
```

### 5. Create Superuser (Optional)
```bash
make superuser
```

### 6. Access the Application
- **Frontend**: http://localhost
- **API Docs**: http://localhost/docs
- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Flower**: http://localhost:5555
- **PgAdmin**: http://localhost:5050

## 📁 Project Structure

```
protmonetlka/
├── backend/
│   ├── app/
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── repositories/   # Data access layer
│   │   ├── services/       # Business logic
│   │   ├── api/            # API endpoints
│   │   ├── tasks/          # Celery tasks
│   │   └── utils/          # Utilities
│   ├── migrations/         # Alembic migrations
│   ├── tests/              # Tests
│   ├── scripts/            # Utility scripts
│   └── pyproject.toml      # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML
│   ├── manifest.json       # PWA manifest
│   ├── css/                # Stylesheets
│   └── js/                 # JavaScript
│       ├── api/            # API clients
│       └── app/            # Application logic
├── docker/
│   ├── api/                # API Dockerfile
│   ├── nginx/              # Nginx configuration
│   ├── prometheus/         # Prometheus config
│   ├── grafana/            # Grafana dashboards
│   ├── loki/               # Loki configuration
│   └── promtail/           # Promtail configuration
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
├── docker-compose.yml      # Development compose
├── docker-compose.prod.yml # Production compose
├── Makefile                # Common commands
└── README.md
```

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (returns tokens)
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/password-reset/request` - Request password reset
- `POST /api/v1/auth/password-reset/confirm` - Confirm password reset

### Users
- `GET /api/v1/users/me` - Get user profile
- `PATCH /api/v1/users/me` - Update profile
- `POST /api/v1/users/me/change-password` - Change password
- `DELETE /api/v1/users/me` - Delete account

### Daily Entries
- `GET /api/v1/entries` - List entries (with date filters)
- `POST /api/v1/entries` - Create entry
- `GET /api/v1/entries/{id}` - Get entry
- `PATCH /api/v1/entries/{id}` - Update entry
- `DELETE /api/v1/entries/{id}` - Delete entry

### Investments
- `GET /api/v1/investments` - List investments
- `POST /api/v1/investments` - Create investment
- `GET /api/v1/investments/summary` - Get summary by type
- `GET /api/v1/investments/{id}` - Get investment
- `PATCH /api/v1/investments/{id}` - Update investment
- `DELETE /api/v1/investments/{id}` - Delete investment

### Goals
- `GET /api/v1/goals/monthly/{year}/{month}` - Get monthly goal
- `PUT /api/v1/goals/monthly/{year}/{month}` - Update monthly goal
- `GET /api/v1/goals/yearly/{year}` - Get yearly goals

### Analytics
- `GET /api/v1/analytics/dashboard` - Dashboard statistics
- `GET /api/v1/analytics/monthly/{year}/{month}` - Monthly analytics
- `GET /api/v1/analytics/annual/{year}` - Annual analytics

### Notifications
- `GET /api/v1/notifications` - List notifications
- `GET /api/v1/notifications/unread/count` - Unread count
- `POST /api/v1/notifications/{id}/read` - Mark as read
- `POST /api/v1/notifications/read-all` - Mark all as read
- `DELETE /api/v1/notifications/{id}` - Delete notification

## 💾 Database Models

### User
- Email, username, password (hashed)
- Full name, active status, superuser flag
- Last login timestamp
- Soft delete support

### DailyEntry
- Date, income, expense (with category)
- Gold/silver grams
- Descriptions and notes
- User relationship

### Investment
- Type (gold, silver, stocks, crypto, etc.)
- Amount, quantity, purchase date
- Current value (updated by background tasks)
- User relationship

### MonthlyGoal
- Year, month
- Income, gold, silver, investment goals
- User relationship

### Notification
- Title, message, type
- Read status
- User relationship

## 📊 Default Monthly Goals

- **Income**: 20,000 PLN
- **Gold**: 10g
- **Silver**: 500g
- **Investments**: 5,100 PLN

## 📝 Expense Categories

- FOOD - Żywność
- TRANSPORT - Transport
- ENTERTAINMENT - Rozrywka
- HOUSING - Mieszkanie
- UTILITIES - Rachunki
- HEALTHCARE - Zdrowie
- EDUCATION - Edukacja
- SHOPPING - Zakupy
- SUBSCRIPTIONS - Subskrypcje
- OTHER - Inne

## 💎 Investment Types

- GOLD - Złoto
- SILVER - Srebro
- STOCKS - Akcje
- BONDS - Obligacje
- CRYPTO - Kryptowaluty
- ETF - ETF
- REAL_ESTATE - Nieruchomości
- SAVINGS - Oszczędności
- OTHER - Inne

## 🛠️ Development

### Local Setup
```bash
# Install dependencies
cd backend
pip install -e ".[dev]"

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Running Tests
```bash
make test          # Run all tests
make test-cov      # Run tests with coverage
```

### Code Quality
```bash
make format        # Format code with black
make lint          # Lint with flake8 and mypy
```

### Database Operations
```bash
make migrate                    # Apply migrations
make migrate-create MSG="..."   # Create new migration
make migrate-down               # Rollback last migration
make db-shell                   # Open PostgreSQL shell
make backup-db                  # Backup database
```

### Celery Tasks
```bash
make logs-celery               # View Celery logs
```

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| api | 8000 | FastAPI application |
| postgres | 5432 | PostgreSQL 16 |
| redis | 6379 | Redis 7 |
| celery_worker | - | Celery worker |
| celery_beat | - | Celery scheduler |
| flower | 5555 | Celery monitoring |
| nginx | 80/443 | Reverse proxy |
| prometheus | 9090 | Metrics |
| grafana | 3000 | Dashboards |
| loki | 3100 | Log aggregation |
| promtail | - | Log shipping |
| pgadmin | 5050 | DB admin |

## 🔒 Security Features

- **JWT Authentication** with access and refresh tokens
- **Password Hashing** with bcrypt (12 rounds)
- **Rate Limiting** (configurable per endpoint)
- **CORS** protection
- **Input Validation** with Pydantic
- **SQL Injection** protection via SQLAlchemy
- **XSS** protection in frontend
- **Secure Headers** via Nginx

## 📈 Monitoring

- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **Loki** - Centralized logging
- **Structured Logs** - JSON format for easy parsing
- **Health Checks** - `/health` endpoint
- **Flower** - Celery task monitoring

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📦 Deployment

### Production Deployment
```bash
# Build and start production services
make prod-build
make prod-up

# View logs
make logs

# Stop services
make prod-down
```

### Environment Variables
See `.env.example` for all available configuration options.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **srccoderre** - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- SQLAlchemy team for the ORM
- Chart.js for visualization
- All open-source contributors

## 📞 Support

For issues and questions, please use the GitHub issue tracker.

---

**Built with ❤️ using modern Python and JavaScript**