CREATE INDEX idx_memberships_email ON memberships (email);

DROP INDEX idx_membership_id ON memberships;

CREATE INDEX idx_plans_provider_price ON plans (provider, price_per_month);

ALTER TABLE accounts ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0;
UPDATE accounts SET is_admin = 1 WHERE LOWER(username) = 'longdepzaii';

ANALYZE TABLE accounts, memberships, plans;
