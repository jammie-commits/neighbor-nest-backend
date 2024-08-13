import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';
import { useParams } from 'react-router-dom';

const EventDetail = () => {
    const { event_id } = useParams();
    const [event, setEvent] = useState(null);

    useEffect(() => {
        const fetchEvent = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get(`/events/${event_id}`);
                setEvent(response.data);
            } catch (error) {
                console.error('Error fetching event:', error);
            }
        };

        fetchEvent();
    }, [event_id]);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
            <div className="max-w-3xl w-full bg-white shadow-lg rounded-lg p-6">
                <h1 className="text-4xl font-bold text-blue-700 mb-4">Event Details</h1>
                {event ? (
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-800 mb-2">{event.title}</h2>
                        <p className="text-lg text-gray-600 mb-4">{event.description}</p>
                        <div className="mb-4">
                            <p className="text-md font-medium text-gray-700">Date:</p>
                            <p className="text-md text-gray-600">{new Date(event.date).toLocaleDateString()}</p>
                        </div>
                        <div className="mb-4">
                            <p className="text-md font-medium text-gray-700">Location:</p>
                            <p className="text-md text-gray-600">{event.location}</p>
                        </div>
                        {/* Render additional event details here */}
                    </div>
                ) : (
                    <p className="text-lg text-gray-500">Loading...</p>
                )}
            </div>
        </div>
    );
};

export default EventDetail;
