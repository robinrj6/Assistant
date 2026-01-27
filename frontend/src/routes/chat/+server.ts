import type { RequestHandler } from './$types';
let path= 'http://localhost:8000'

export const POST: RequestHandler = async (event) => {
    const { prompt } = await event.request.json();
    const res = await fetch(`${ path }/chat` , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
    });
    // Proxy the NDJSON stream directly to the client.
    return new Response(res.body, {
        headers: {
            'Content-Type': 'application/x-ndjson'
        }
    });
};