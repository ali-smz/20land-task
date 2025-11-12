# پروژه Bistland - سیستم ثبت شماره موبایل

این پروژه یک سیستم Landing Page برای ثبت شماره موبایل کاربران است که از معماری Full-Stack استفاده می‌کند.

## معماری پروژه

### Backend

- **فریمورک**: Django 5.2.8 + Django REST Framework
- **دیتابیس**: PostgreSQL (ذخیره‌سازی شماره موبایل‌ها)
- **دیتابیس Log**: MongoDB (ذخیره‌سازی لاگ‌های درخواست‌ها)
- **Queue System**: Celery + Redis (برای پردازش غیرهمزمان)
- **Web Server**: Gunicorn

### Frontend

- **فریمورک**: React 18.2
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Notifications**: React Toastify

## ویژگی‌ها

- ✅ ثبت شماره موبایل با اعتبارسنجی
- ✅ Rate Limiting (محدودیت 20 درخواست بر ثانیه)
- ✅ لاگ‌گیری تمام درخواست‌ها در MongoDB
- ✅ پردازش غیرهمزمان با Celery
- ✅ رابط کاربری زیبا با ویدیو پس‌زمینه
- ✅ پشتیبانی از RTL برای فارسی
- ✅ مدیریت خطا و نمایش پیام‌های مناسب

## پیش‌نیازها

- Docker و Docker Compose
- Python 3.12+
- Node.js 20+

## نصب و راه‌اندازی

### 1. کلون کردن پروژه

```bash
git clone <repository-url>
cd bistland
```

### 2. ایجاد فایل .env

فایل `env.example` را به `.env` کپی کنید و مقادیر را تنظیم کنید:

```bash
cp env.example .env
```

سپس فایل `.env` را ویرایش کرده و مقادیر مناسب را تنظیم کنید:

```env
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=*
MONGO_URI=mongodb://mongo:27017/
MONGO_DB=landing_logs
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

### 3. راه‌اندازی با Docker Compose

```bash
docker-compose up --build
```

این دستور تمام سرویس‌های زیر را راه‌اندازی می‌کند:

- Backend API (پورت 8000)
- Frontend (پورت 3000)
- PostgreSQL (پورت 5432)
- Redis (پورت 6379)
- MongoDB (پورت 27017)
- Celery Worker

### 4. اجرای Migrations

```bash
docker-compose exec backend python manage.py migrate
```

### 5. ایجاد Superuser (اختیاری)

```bash
docker-compose exec backend python manage.py createsuperuser
```

## دسترسی به سرویس‌ها

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **MongoDB**: localhost:27017

## API Endpoints

### ثبت شماره موبایل

```
POST /api/submit/
Content-Type: application/json

{
  "mobile": "09123456789"
}
```

**Response:**

```json
{
  "status": "ok"
}
```

## ساختار پروژه

```
bistland/
├── backend/                 # Django Backend
│   ├── config/             # تنظیمات Django
│   │   ├── settings.py     # تنظیمات اصلی
│   │   ├── urls.py         # URL Routing
│   │   └── celery.py       # تنظیمات Celery
│   ├── landing/            # اپلیکیشن Landing
│   │   ├── models.py       # مدل‌های دیتابیس
│   │   ├── views.py        # View Functions
│   │   ├── serializers.py  # API Serializers
│   │   ├── tasks.py        # Celery Tasks
│   │   ├── middleware.py   # Request Logging Middleware
│   │   └── middleware_rate.py  # Rate Limiting Middleware
│   ├── requirements.txt    # Python Dependencies
│   └── Dockerfile          # Docker Image برای Backend
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── App.jsx         # کامپوننت اصلی
│   │   └── components/     # کامپوننت‌های React
│   ├── package.json        # Node Dependencies
│   └── Dockerfile          # Docker Image برای Frontend
└── docker-compose.yml      # Docker Compose Configuration
```

## توسعه محلی

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Celery Worker

```bash
cd backend
celery -A config worker -l info
```

## Rate Limiting

پروژه از Rate Limiting استفاده می‌کند که محدودیت 20 درخواست بر ثانیه برای هر IP را اعمال می‌کند. در صورت تجاوز از این محدودیت، پاسخ `429 Too Many Requests` برگردانده می‌شود.

## لاگ‌گیری

تمام درخواست‌های HTTP در MongoDB ذخیره می‌شوند و شامل اطلاعات زیر هستند:

- Path و Method
- IP Address
- User Agent
- Timestamp

همچنین اطلاعات مربوط به ثبت شماره موبایل (IP و User Agent) نیز در MongoDB ذخیره می‌شود.

## امنیت

- ✅ Rate Limiting برای جلوگیری از حملات DDoS
- ✅ CORS Configuration
- ✅ اعتبارسنجی شماره موبایل در سمت سرور
- ⚠️ برای Production، `DEBUG=False` و `SECRET_KEY` امن تنظیم کنید
- ⚠️ از Environment Variables برای اطلاعات حساس استفاده کنید

## مشکلات رایج

### مشکل اتصال به دیتابیس

- مطمئن شوید که PostgreSQL در حال اجرا است
- تنظیمات دیتابیس در `.env` را بررسی کنید

### مشکل Celery

- مطمئن شوید که Redis در حال اجرا است
- Worker Celery را بررسی کنید: `docker-compose logs celery`

### مشکل CORS

- تنظیمات `CORS_ALLOW_ALL_ORIGINS` در `settings.py` را بررسی کنی
