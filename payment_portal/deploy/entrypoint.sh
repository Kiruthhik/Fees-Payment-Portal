#!/usr/bin/env bash
set -e

echo "=== Starting Django container ==="

# Wait for DB
if [ -n "$DB_HOST" ]; then
  echo "Waiting for database at $DB_HOST..."
  python - <<PY
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
        print(f"⏳ Waiting for DB ({i+1}/60)...")
        time.sleep(2)
else:
    print("❌ Database not reachable, exiting.")
    sys.exit(1)
PY
fi

echo "⚙️ Applying database migrations..."
python manage.py migrate --noinput || { echo "❌ Migration failed"; exit 1; }

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput || { echo "❌ Static collection failed"; exit 1; }

echo "🚀 Starting Gunicorn..."
exec gunicorn payment_portal.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --log-level debug \
  --access-logfile - \
  --error-logfile -
