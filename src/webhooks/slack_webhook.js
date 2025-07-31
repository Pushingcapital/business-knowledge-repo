// Slack Event Webhook Receiver
// Deploy to Cloudflare Workers

export default {
  async fetch(request, env, ctx) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const data = await request.json();
      
      // Handle Slack URL verification
      if (data.type === 'url_verification') {
        return new Response(data.challenge);
      }
      
      // Process Slack events
      if (data.type === 'event_callback') {
        await processSlackEvent(data.event, env);
      }

      return new Response('OK', { status: 200 });
    } catch (error) {
      console.error('Slack webhook error:', error);
      return new Response('Error', { status: 500 });
    }
  }
};

async function processSlackEvent(event, env) {
  // Capture important business conversations
  if (shouldCaptureMessage(event)) {
    const businessData = {
      timestamp: new Date().toISOString(),
      channel: event.channel,
      user: event.user,
      text: event.text,
      thread_ts: event.thread_ts || null,
      type: 'slack_message'
    };

    // Forward to HubSpot if it mentions deals/clients
    if (containsBusinessKeywords(event.text)) {
      await createHubSpotActivity(businessData, env.HUBSPOT_API_TOKEN);
    }

    // Log to knowledge repo
    await logToKnowledgeRepo(businessData);
  }
}

function shouldCaptureMessage(event) {
  // Don't capture bot messages or edited messages
  if (event.bot_id || event.subtype === 'message_changed') {
    return false;
  }
  
  // Capture messages with business keywords
  const businessKeywords = [
    'deal', 'client', 'quote', 'revenue', 'payment', 
    'contract', 'proposal', 'meeting', 'follow up',
    'credit', 'vehicle', 'transport', 'funding'
  ];
  
  return businessKeywords.some(keyword => 
    event.text?.toLowerCase().includes(keyword)
  );
}

function containsBusinessKeywords(text) {
  const keywords = ['deal', 'client', 'quote', 'payment', 'contract'];
  return keywords.some(keyword => text?.toLowerCase().includes(keyword));
}

async function createHubSpotActivity(data, token) {
  if (!token) return;
  
  const activity = {
    properties: {
      hs_activity_type: 'NOTE',
      hs_body: `Slack Discussion: ${data.text}`,
      hs_timestamp: new Date(data.timestamp).getTime()
    }
  };

  await fetch('https://api.hubapi.com/crm/v3/objects/activities', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(activity)
  });
}

async function logToKnowledgeRepo(data) {
  console.log('Business Slack Message:', JSON.stringify(data));
}
