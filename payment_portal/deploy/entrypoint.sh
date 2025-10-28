#!/bin/sh
set -e

# Optional: Wait for the Azure SQL Database to be reachable before running migrations
if [ -n "$DB_HOST" ]; then
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  python - <<'PY'
import socket, time, os, sys
host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT', '1433'))
for i in range(60):
    try:
        s = socket.create_connection((host, port), timeout=5)
        s.close()
        print("✅ Database reachable.")
        break
    except Exception:
        print(f"⏳ Waiting for DB... attempt {i+1}")
        time.sleep(2)
else:
    print("❌ Database not reachable, exiting.")
    sys.exit(1)
PY
fi

# Apply DB migrations
echo "🚀 Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Optional: You could auto-create superuser for dev (commented out)
# echo "Creating default admin user (dev only)..."
# python manage.py shell -c "from django.contrib.auth import get_user_model; \
# User = get_user_model(); \
# User.objects.filter(username='admin').exists() or \
# User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"

# Start Gunicorn
echo "🔥 Starting Gunicorn..."
exec gunicorn payment_portal.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --timeout 120
