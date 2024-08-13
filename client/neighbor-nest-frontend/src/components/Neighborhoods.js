import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';

const Neighborhoods = () => {
    const [neighborhoods, setNeighborhoods] = useState([]);

    useEffect(() => {
        const fetchNeighborhoods = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get('/neighborhoods');
                setNeighborhoods(response.data);
            } catch (error) {
                console.error('Error fetching neighborhoods:', error);
            }
        };

        fetchNeighborhoods();
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="container mx-auto max-w-4xl bg-white shadow-md rounded-lg p-6">
                <h1 className="text-3xl font-bold mb-6 text-gray-800">Neighborhoods</h1>
                <ul className="space-y-4">
                    {neighborhoods.map(neighborhood => (
                        <li
                            key={neighborhood.neighborhood_id}
                            className="p-4 border border-gray-300 rounded-lg shadow-sm bg-white hover:bg-gray-50 transition ease-in-out duration-150"
                        >
                            <h2 className="text-xl font-semibold text-gray-800">{neighborhood.name}</h2>
                            <p className="text-gray-600 mt-2">{neighborhood.description}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Neighborhoods;
