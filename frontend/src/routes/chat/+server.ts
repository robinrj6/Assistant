import type { RequestHandler } from './$types';
let path= 'http://localhost:8000'

export const POST: RequestHandler = async (event) => {
    const body = await event.request.json();
    const { prompt, convo_id } = body;
    const res = await fetch(`${ path }/chat` , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, convo_id }),
    });
    // Proxy the NDJSON stream directly to the client.
    return new Response(res.body, {
        headers: {
            'Content-Type': 'application/x-ndjson'
        }
    });
};