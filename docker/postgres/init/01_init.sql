-- Initialize PostgreSQL database
-- This script runs when the container is first created

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'Europe/Warsaw';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE portfel_db TO portfel;
