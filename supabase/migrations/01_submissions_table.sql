-- Migration: Create Submissions Table
CREATE TABLE submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idempotency_key UUID UNIQUE NOT NULL,
  source TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- Note: Anonymous users insert into this table. 
-- For production, this requires an INSERT policy allowing anon roles,
-- or bypassing RLS completely via a service-role key in the Edge Function.
-- We are using the service-role key in the Edge Function, so RLS doesn't block it.
