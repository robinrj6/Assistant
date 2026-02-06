import type { RequestHandler } from './$types';

const path = 'http://localhost:8000';

export const GET: RequestHandler = async () => {
	const res = await fetch(`${path}/chat/history`, {
		method: 'GET'
	});

	return new Response(res.body, {
		status: res.status,
		headers: {
			'Content-Type': res.headers.get('content-type') ?? 'application/json'
		}
	});
};