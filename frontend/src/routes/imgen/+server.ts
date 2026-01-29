import type { RequestHandler } from './$types';
let path= 'http://localhost:8000'

export const POST: RequestHandler = async (event) => {
    const formData = await event.request.formData();

    // Rename file field to match backend expectation
    const file = formData.get('Cimage');

    const res = await fetch(`${path}/images/generate`, {
        method: 'POST',
        body: formData
    });

    const responseData = await res.json();
    
    // Return the response as JSON (the image path or error message)
    return new Response(JSON.stringify(responseData), {
        headers: {
            'Content-Type': 'application/json'
        },
        status: res.status
    });
};