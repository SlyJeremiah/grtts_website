#!/bin/bash
set -euo pipefail

echo "=== GRTTS build ==="

pip install -r requirements.txt

# Applies any unapplied migrations. Migrations are additive by design — review
# every generated migration before merging; this runs automatically on deploy.
#
# Only production deploys migrate. Every pull request builds a preview, and a
# preview build runs with whatever DATABASE_URL is in scope: if that variable
# is not restricted to the Production environment in Vercel, an unmerged
# branch would migrate the live database. Opening a PR should not alter
# production data.
#
# If you give previews their own database, set RUN_MIGRATIONS=1 on the Preview
# environment so that database gets migrated too.
if [ "${VERCEL_ENV:-}" = "production" ] || [ "${RUN_MIGRATIONS:-}" = "1" ]; then
  echo "=== Applying migrations (VERCEL_ENV=${VERCEL_ENV:-unset}) ==="
  python manage.py migrate --no-input
else
  echo "=== Skipping migrations on ${VERCEL_ENV:-unknown} deployment ==="
  echo "    Set RUN_MIGRATIONS=1 to migrate this environment's database."
  # Report what would have run, so a pending migration shows up in the build
  # log rather than being discovered after the merge. Read-only, and never
  # fatal: a preview that cannot reach a database should still build.
  if plan=$(python manage.py showmigrations --plan 2>/dev/null); then
    pending=$(printf '%s\n' "$plan" | grep -c '^\[ \]' || true)
    echo "    ${pending} migration(s) would be applied on the next production deploy."
  else
    echo "    Could not read migration state (no database reachable from this build)."
  fi
fi

# static/ is committed and served by Vercel's CDN. collectstatic only populates
# staticfiles/ for WhiteNoise as a fallback; --clear is deliberately not used.
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Build complete ==="
