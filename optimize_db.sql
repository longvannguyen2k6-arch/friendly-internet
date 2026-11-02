-- Optional performance/integrity tweaks for the `webprogramming` database.
-- Run once (MySQL 8):  mysql -u root -p webprogramming < optimize_db.sql
-- BACK UP the database first. Each statement is independent; if one fails
-- because the index/constraint already exists, just continue with the next.

-- Membership lookup by e-mail (membership_lookup / membership_result pages)
CREATE INDEX idx_memberships_email ON memberships (email);

-- The UNIQUE key on memberships.membership_id already serves lookups, so the
-- second, duplicate index is pure write overhead:
DROP INDEX idx_membership_id ON memberships;

-- Recommendation query filters by provider and sorts by price
CREATE INDEX idx_plans_provider_price ON plans (provider, price_per_month);

-- Admin flag on accounts (instead of only hard-coding a username)
ALTER TABLE accounts ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0;
UPDATE accounts SET is_admin = 1 WHERE LOWER(username) = 'longdepzaii';

-- Refresh optimizer statistics
ANALYZE TABLE accounts, memberships, plans;
