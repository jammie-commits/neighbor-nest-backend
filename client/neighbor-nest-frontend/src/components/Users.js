import React, { useEffect, useState } from 'react';
import { api, setAuthHeader } from '../api/api';

const Users = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            const token = localStorage.getItem('token');
            setAuthHeader(token);

            try {
                const response = await api.get('/users');
                setUsers(response.data);
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        };

        fetchUsers();
    }, []);

    return (
        <div className="min-h-screen bg-gray-100 py-6 px-4">
            <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-lg p-8">
                <h1 className="text-3xl font-bold mb-6 text-gray-800">Users</h1>
                {users.length > 0 ? (
                    <ul className="space-y-4">
                        {users.map(user => (
                            <li
                                key={user.user_id}
                                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg shadow-sm hover:bg-gray-100 transition"
                            >
                                <div className="text-gray-700">
                                    <p className="text-lg font-semibold">{user.name}</p>
                                    <p className="text-sm text-gray-500">{user.email}</p>
                                </div>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="text-lg text-gray-500">No users found.</p>
                )}
            </div>
        </div>
    );
};

export default Users;
