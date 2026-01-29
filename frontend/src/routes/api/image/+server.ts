import { readFileSync } from 'fs';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
    const filePath = url.searchParams.get('path');
    
    if (!filePath) {
        return new Response('Missing path parameter', { status: 400 });
    }
    
    try {
        const fileBuffer = readFileSync(filePath);
        return new Response(fileBuffer, {
            headers: {
                'Content-Type': 'image/png'
            }
        });
    } catch (error) {
        return new Response('File not found', { status: 404 });
    }
};
