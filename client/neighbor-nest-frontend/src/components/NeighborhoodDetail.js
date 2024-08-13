import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';
import { useParams } from 'react-router-dom';

const NeighborhoodDetail = () => {
    const { neighborhood_id } = useParams();
    const [neighborhood, setNeighborhood] = useState(null);

    useEffect(() => {
        const fetchNeighborhood = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get(`/neighborhoods/${neighborhood_id}`);
                setNeighborhood(response.data);
            } catch (error) {
                console.error('Error fetching neighborhood:', error);
            }
        };

        fetchNeighborhood();
    }, [neighborhood_id]);

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="container mx-auto max-w-4xl bg-white shadow-md rounded-lg p-6">
                <h1 className="text-3xl font-bold mb-4 text-gray-800">Neighborhood Details</h1>
                {neighborhood ? (
                    <div>
                        <h2 className="text-2xl font-semibold text-gray-700 mb-2">{neighborhood.name}</h2>
                        <p className="text-gray-600">{neighborhood.description}</p>
                        {/* Render additional neighborhood details here */}
                    </div>
                ) : (
                    <p className="text-gray-500">Loading...</p>
                )}
            </div>
        </div>
    );
};

export default NeighborhoodDetail;
