#!/bin/bash
set -euo pipefail

echo "=== GRTTS build ==="

pip install -r requirements.txt

# Applies any unapplied migrations. Migrations are additive by design — review
# every generated migration before merging; this runs automatically on deploy.
#
# Preview deploys do not migrate. Every pull request builds a preview, and a
# preview build runs with whatever DATABASE_URL is in scope: if that variable
# is not restricted to the Production environment in Vercel, an unmerged
# branch would migrate the live database. Opening a PR should not alter
# production data.
#
# VERCEL_ENV is what distinguishes the two, and it is a Vercel *system*
# variable: a project with "Automatically expose System Environment Variables"
# switched off never receives it. The first version of this guard tested
# `VERCEL_ENV = production` directly, so on this project the variable was
# absent, every production deploy quietly skipped its migrations, and the
# courses page went live with nothing in it.
#
# So an absent VERCEL_ENV now means "assume production and migrate". The worst
# case is the behaviour this script had before the guard existed; the
# alternative is a production deploy that silently does not migrate, which is
# far harder to notice. Migrations are skipped only when Vercel positively
# says this is not a production deployment.
#
# Overrides, for when the default is wrong:
#   RUN_MIGRATIONS=1   migrate anyway — a preview with its own database
#   SKIP_MIGRATIONS=1  never migrate — previews sharing the production
#                      database on a project with system variables switched off
DEPLOY_ENV="${VERCEL_ENV:-production}"

if [ "${SKIP_MIGRATIONS:-}" = "1" ]; then
  echo "=== Skipping migrations: SKIP_MIGRATIONS=1 ==="
elif [ "$DEPLOY_ENV" = "production" ] || [ "${RUN_MIGRATIONS:-}" = "1" ]; then
  echo "=== Applying migrations (VERCEL_ENV=${VERCEL_ENV:-unset, assuming production}) ==="
  python manage.py migrate --no-input
else
  echo "=== Skipping migrations on ${DEPLOY_ENV} deployment ==="
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
