interface ImgGenResponse {
    image_url: string;
}

interface HistoryItem {
		convo_id: string;
		role: string;
		content: string;
	}

interface HistoryArray {
        history: HistoryItem[];
}

export type { ImgGenResponse, HistoryItem, HistoryArray };