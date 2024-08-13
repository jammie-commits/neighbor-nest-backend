import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import { api } from '../api/api';
import Navbar from './Navbar';

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
            {/* Navbar Component */}
            {/* <Navbar /> */}

            {/* Welcoming Section */}
            <section className="bg-gray-900 bg-opacity-70 p-8 text-center text-white">
                <h1 className="text-4xl font-bold mb-4">Welcome to Our Community</h1>
                <p className="text-xl">Explore the latest events happening in your neighborhood!</p>
            </section>

            {/* Events Gallery */}
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
