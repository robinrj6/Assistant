import type { RequestHandler } from '@sveltejs/kit';

// POST /chat: send a default "Hello" prompt to backend and
// aggregate the streaming NDJSON into a single message.
export const POST: RequestHandler = async ({ fetch }) => {
    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'accept': 'application/x-ndjson' , 'Access-Control-Allow-Origin': '*' },
            body: JSON.stringify({ prompt: 'Hello!' })
        });

        console.log('Response status:', response.status);

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let message = '';

        if (!reader) {
            return new Response(JSON.stringify({ message }), {
                headers: { 'Content-Type': 'application/json' }
            });
        }

        // Read stream and parse JSON objects (separated by newlines or concatenated)
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            // Try to extract complete JSON objects from buffer
            let lastValidIndex = -1;
            let braceCount = 0;
            let inString = false;
            let escaped = false;

            for (let i = 0; i < buffer.length; i++) {
                const char = buffer[i];

                if (escaped) {
                    escaped = false;
                    continue;
                }

                if (char === '\\') {
                    escaped = true;
                    continue;
                }

                if (char === '"' && !escaped) {
                    inString = !inString;
                    continue;
                }

                if (!inString) {
                    if (char === '{') braceCount++;
                    else if (char === '}') {
                        braceCount--;
                        if (braceCount === 0) {
                            lastValidIndex = i;
                        }
                    }
                }
            }

            // Process all complete JSON objects found
            if (lastValidIndex >= 0) {
                const jsonStr = buffer.substring(0, lastValidIndex + 1);
                buffer = buffer.substring(lastValidIndex + 1);

                // Try to parse multiple objects from the string
                const objects = jsonStr.match(/\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}/g) || [];
                for (const obj of objects) {
                    try {
                        const parsed = JSON.parse(obj);
                        if (typeof parsed.response === 'string') {
                            message += parsed.response;
                        }
                    } catch {
                        // ignore malformed fragments
                    }
                }
            }
        }

        return new Response(JSON.stringify({ message }), {
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : 'Unknown error';
        return new Response(JSON.stringify({ error: msg }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};