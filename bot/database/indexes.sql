-- ============================================
-- bot/database/indexes.sql
-- הרצה: sqlite3 bot.db < bot/database/indexes.sql
-- ============================================
CREATE INDEX IF NOT EXISTS idx_users_language ON users(language);
CREATE INDEX IF NOT EXISTS idx_users_referred_by ON users(referred_by);
CREATE INDEX IF NOT EXISTS idx_pension_profiles_user ON pension_profiles(telegram_id);
CREATE INDEX IF NOT EXISTS idx_events_log_user ON events_log(user_id);
CREATE INDEX IF NOT EXISTS idx_events_log_type ON events_log(event_type);
CREATE INDEX IF NOT EXISTS idx_events_log_timestamp ON events_log(timestamp);
