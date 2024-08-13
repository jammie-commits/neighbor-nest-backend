import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';
import { useParams } from 'react-router-dom';

const NewsDetail = () => {
    const { news_id } = useParams();
    const [newsItem, setNewsItem] = useState(null);

    useEffect(() => {
        const fetchNewsItem = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get(`/news/${news_id}`);
                setNewsItem(response.data);
            } catch (error) {
                console.error('Error fetching news item:', error);
            }
        };

        fetchNewsItem();
    }, [news_id]);

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="container mx-auto max-w-3xl bg-white shadow-lg rounded-lg p-6">
                <h1 className="text-3xl font-bold mb-6 text-gray-800">News Details</h1>
                {newsItem ? (
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-900 mb-4">{newsItem.title}</h2>
                        <p className="text-gray-700 whitespace-pre-wrap">{newsItem.content}</p>
                        {/* Render additional news details here */}
                    </div>
                ) : (
                    <p className="text-gray-500">Loading...</p>
                )}
            </div>
        </div>
    );
};

export default NewsDetail;
