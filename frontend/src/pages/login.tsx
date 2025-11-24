import React, { useState } from "react";
import { login as loginApi } from "../api/auth"
import { useAuth } from "../context/AuthContext"

const Login: React.FC = () => {
    const { login } = useAuth();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const response = await loginApi({ username, password });
            login(response.access_token); // save token to context + localStorage.
        } catch (err) {
            setError("Invalid username or password");
        }
    }

    return (
        <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
            <form
                onSubmit={handleSubmit}
                style={{ display: "flex", flexDirection: "column", width: "300px" }}
            >
                <h2>Login</h2>

                {error && <p style={{ color: "red" }}>{error}</p>}

                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    style={{ marginBottom: "10px", padding: "8px" }}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ marginBottom: "10px", padding: "8px" }}
                />

                <button type="submit" style={{ padding: "8px" }}>
                    Login
                </button>
            </form>
        </div>
    );
};

export default Login;