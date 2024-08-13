import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';

const Dashboard = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get('/protected'); // Assuming '/protected' returns user data
                setUserData(response.data);
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        fetchUserData();
    }, []);

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="p-6 bg-white shadow-md rounded-lg max-w-md w-full">
                <h1 className="text-3xl font-bold text-blue-600 mb-4">Dashboard</h1>
                {userData ? (
                    <div>
                        <p className="text-lg text-gray-700">Welcome, {userData.message}!</p>
                        {/* Render additional user data here */}
                    </div>
                ) : (
                    <p className="text-lg text-gray-500">Loading...</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
