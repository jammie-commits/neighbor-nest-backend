import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';

const News = () => {
    const [news, setNews] = useState([]);

    useEffect(() => {
        const fetchNews = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get('/news');
                setNews(response.data);
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        };

        fetchNews();
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="container mx-auto max-w-4xl bg-white shadow-md rounded-lg p-6">
                <h1 className="text-3xl font-bold mb-6 text-gray-800">News</h1>
                <ul className="space-y-4">
                    {news.map(newsItem => (
                        <li
                            key={newsItem.news_id}
                            className="p-4 border border-gray-300 rounded-lg shadow-sm bg-white hover:bg-gray-50 transition ease-in-out duration-150"
                        >
                            <h2 className="text-xl font-semibold text-gray-800">{newsItem.title}</h2>
                            <p className="text-gray-600 mt-2">{newsItem.status}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default News;
