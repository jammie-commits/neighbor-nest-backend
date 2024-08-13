import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';

const Events = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get('/events');
                setEvents(response.data);
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        fetchEvents();
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 p-4">
            <h1 className="text-3xl font-bold text-blue-600 mb-6">Upcoming Events</h1>
            {events.length > 0 ? (
                <ul className="space-y-4">
                    {events.map(event => (
                        <li key={event.event_id} className="bg-white shadow-md rounded-lg p-4">
                            <h2 className="text-2xl font-semibold text-gray-800 mb-2">{event.title}</h2>
                            <p className="text-lg text-gray-600 mb-1">Date: {new Date(event.date).toLocaleDateString()}</p>
                            <p className="text-md text-gray-500">Location: {event.location}</p>
                            {/* Add more details as needed */}
                        </li>
                    ))}
                </ul>
            ) : (
                <p className="text-lg text-gray-500">No events available.</p>
            )}
        </div>
    );
};

export default Events;
