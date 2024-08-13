import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';
import { useParams } from 'react-router-dom';

const UserDetail = () => {
    const { user_id } = useParams();
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get(`/users/${user_id}`);
                setUser(response.data);
            } catch (error) {
                console.error('Error fetching user:', error);
            }
        };

        fetchUser();
    }, [user_id]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 py-6 px-4">
            <div className="w-full max-w-lg bg-white shadow-lg rounded-lg p-8">
                <h1 className="text-3xl font-bold mb-6 text-gray-800">User Details</h1>
                {user ? (
                    <div>
                        <p className="text-lg font-medium text-gray-700">Name: <span className="font-normal">{user.name}</span></p>
                        <p className="text-lg font-medium text-gray-700 mt-4">Email: <span className="font-normal">{user.email}</span></p>
                        {/* Render additional user details here */}
                    </div>
                ) : (
                    <p className="text-lg text-gray-500">Loading...</p>
                )}
            </div>
        </div>
    );
};

export default UserDetail;
