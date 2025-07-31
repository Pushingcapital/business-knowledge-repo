// OpenPhone Webhook Receiver
// Deploy to Cloudflare Workers for reliable webhook handling

export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const data = await request.json();
      
      // Process OpenPhone webhook data
      const event = {
        type: data.type, // 'call', 'sms', 'voicemail'
        phone: data.phone_number,
        contact: data.contact_name,
        message: data.message || data.transcription,
        timestamp: new Date().toISOString(),
        duration: data.duration || null
      };

      // Forward to HubSpot (create contact/activity)
      if (env.HUBSPOT_API_TOKEN) {
        await forwardToHubSpot(event, env.HUBSPOT_API_TOKEN);
      }

      // Log to business knowledge repo
      await logToKnowledgeRepo(event);

      return new Response('Webhook processed', { status: 200 });
    } catch (error) {
      console.error('Webhook error:', error);
      return new Response('Webhook error', { status: 500 });
    }
  }
};

async function forwardToHubSpot(event, token) {
  // Create HubSpot activity
  const hubspotData = {
    properties: {
      hs_activity_type: event.type === 'call' ? 'CALL' : 'NOTE',
      hs_body: `${event.type.toUpperCase()}: ${event.message}`,
      hs_timestamp: new Date(event.timestamp).getTime()
    }
  };

  await fetch('https://api.hubapi.com/crm/v3/objects/activities', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(hubspotData)
  });
}

async function logToKnowledgeRepo(event) {
  // This would integrate with your knowledge repo
  // For now, we'll create a simple log format
  const logEntry = {
    timestamp: event.timestamp,
    type: 'openphone_event',
    data: event
  };
  
  console.log('OpenPhone Event:', JSON.stringify(logEntry));
}
