import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import { api } from '../api/api'; // Remove setAuthHeader if not used

const Home = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
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
        <div className="min-h-screen bg-cover bg-center" style={{ backgroundImage: "url('/path-to-your-image.jpg')" }}>
            <header className="bg-gray-900 bg-opacity-70 p-4">
                <div className="container mx-auto flex justify-between items-center">
                    <h1 className="text-white text-2xl font-bold">Event Management</h1>
                    <div>
                        <Link to="/login" className="text-white mr-4 hover:underline">Login</Link>
                        <Link to="/register" className="text-white hover:underline">Register</Link>
                    </div>
                </div>
            </header>

            <section className="container mx-auto p-8">
                <h2 className="text-3xl font-bold text-white text-center mb-8">Past Events</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {events.map(event => (
                        <div key={event.event_id} className="relative bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition duration-300">
                            <img src={event.image_url} alt={event.title} className="w-full h-48 object-cover" />
                            <div className="p-4">
                                <h3 className="font-bold text-xl">{event.title}</h3>
                                <p className="text-gray-600">{event.date}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
};

export default Home;
