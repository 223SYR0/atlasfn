// Vercel Serverless Function for Stripe Payment Intents
// This runs on Vercel's servers (NOT in the browser) so the secret key is safe

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

module.exports = async (req, res) => {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { amount, currency, description, metadata } = req.body;

    // Validate amount
    if (!amount || amount < 50) {
      return res.status(400).json({ error: 'Invalid amount (minimum $0.50)' });
    }

    // Create payment intent with Stripe
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount), // Should already be in cents
      currency: currency || 'usd',
      description: description || 'Atlas FN Purchase',
      metadata: metadata || {},
      automatic_payment_methods: {
        enabled: true,
      },
    });

    // Return client secret to frontend
    res.status(200).json({
      clientSecret: paymentIntent.client_secret,
      paymentIntentId: paymentIntent.id
    });

  } catch (error) {
    console.error('Stripe Error:', error);
    res.status(500).json({ 
      error: error.message || 'Payment intent creation failed' 
    });
  }
};
