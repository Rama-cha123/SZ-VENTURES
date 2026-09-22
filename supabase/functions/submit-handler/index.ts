import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.39.3'

const PRODUCT_PRICES: Record<string, number> = {
  "1": 349,
  "2": 299,
  "3": 399,
  "4": 199,
  "5": 149
};

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, X-Idempotency-Key',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  }

  const idempotencyKey = req.headers.get('X-Idempotency-Key');
  if (!idempotencyKey) {
    return new Response(JSON.stringify({ error: 'Missing X-Idempotency-Key header' }), { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  }

  try {
    const data = await req.json();
    const source = data.source || 'unknown';

    // Backend Validation: Bowl & Sip Checkout
    if (source === 'bowl_and_sip_order') {
      const items = data.items || [];
      let calculatedSubtotal = 0;
      for (const item of items) {
        const itemId = String(item.id);
        const qty = item.qty || 1;
        if (PRODUCT_PRICES[itemId]) {
          calculatedSubtotal += PRODUCT_PRICES[itemId] * qty;
        } else {
          return new Response(JSON.stringify({ error: `Invalid product ID: ${itemId}` }), { status: 400 });
        }
      }
      
      const calculatedTax = Math.round(calculatedSubtotal * 0.05);
      const calculatedDelivery = 49;
      const calculatedTotal = calculatedSubtotal + calculatedTax + calculatedDelivery;
      
      if (parseInt(data.total || '0') !== calculatedTotal) {
        return new Response(JSON.stringify({ error: `Total mismatch. Client: ${data.total}, Server: ${calculatedTotal}` }), { status: 400 });
      }

      data.subtotal = calculatedSubtotal;
      data.tax = calculatedTax;
      data.total = calculatedTotal;
      data.status = 'payment_pending_integration';
    }

    // Initialize Supabase Client for idempotency and storage
    const supabaseUrl = Deno.env.get('SUPABASE_URL') || '';
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') || '';
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Idempotency Check
    const { data: existingData, error: checkError } = await supabase
      .from('submissions')
      .select('*')
      .eq('idempotency_key', idempotencyKey)
      .single();

    if (existingData) {
      // Fast deep compare or hash compare would go here for robust protection
      return new Response(JSON.stringify({ status: 'success', message: 'Cached', id: existingData.id }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
    }

    // Insert
    const { data: insertData, error: insertError } = await supabase
      .from('submissions')
      .insert([
        {
          idempotency_key: idempotencyKey,
          source: source,
          payload: data
        }
      ])
      .select()
      .single();

    if (insertError) throw insertError;

    return new Response(JSON.stringify({ status: 'success', id: insertData.id }), { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } });
  }
});
