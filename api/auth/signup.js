// Supabase Signup API
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

function parseRequestBody(req) {
  if (!req || typeof req.body === 'undefined' || req.body === null) {
    return {};
  }

  if (typeof req.body === 'string') {
    try {
      return JSON.parse(req.body);
    } catch (error) {
      return {};
    }
  }

  return req.body;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    if (!process.env.SUPABASE_URL || !process.env.SUPABASE_KEY) {
      return res.status(500).json({ error: 'Supabase environment variables are missing' });
    }

    const supabaseUrl = process.env.SUPABASE_URL.trim();
    const urlOk = /^https:\/\/[a-z0-9-]+\.supabase\.co\/?$/i.test(supabaseUrl);
    if (!urlOk) {
      return res.status(500).json({ error: 'SUPABASE_URL is invalid. Copy Project URL from Supabase Settings > API.' });
    }

    const { username, email, password } = parseRequestBody(req);

    if (!username || !email || !password) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Create auth user
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          username: username
        }
      }
    });

    if (authError) {
      const message = authError.message || 'Signup failed';
      if (message.toLowerCase().includes('fetch failed')) {
        return res.status(500).json({ error: 'Supabase request failed. Check SUPABASE_URL and try again.' });
      }
      return res.status(400).json({ error: message });
    }

    // Create user profile
    const { data: profile, error: profileError } = await supabase
      .from('users')
      .insert([
        {
          id: authData.user.id,
          username,
          email,
          balance: 0,
          role: 'customer',
          created_at: new Date().toISOString()
        }
      ])
      .select()
      .single();

    if (profileError) {
      return res.status(400).json({ error: profileError.message });
    }

    res.status(200).json({
      user: {
        id: profile.id,
        username: profile.username,
        email: profile.email,
        balance: profile.balance,
        role: profile.role,
        permissions: profile.permissions || []
      },
      session: authData.session || null
    });
  } catch (error) {
    console.error('Signup error:', error);
    res.status(500).json({ error: 'Signup failed' });
  }
};
