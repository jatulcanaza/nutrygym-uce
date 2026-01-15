import axios from "axios";

const API_URL = "http://localhost:3001";

// =======================
// LOGIN
// =======================
export async function loginUser(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);
  formData.append("grant_type", "");
  formData.append("scope", "");
  formData.append("client_id", "");
  formData.append("client_secret", "");

  const response = await axios.post(
    `${API_URL}/auth/login`,
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data; // access_token, refresh_token
}

// =======================
// REGISTER
// =======================
export async function registerUser(
  name: string,
  email: string,
  password: string
) {
  const response = await axios.post(`${API_URL}/auth/register`, {
    name,
    email,
    password,
  });

  return response.data;
}

// =======================
// GET USER INFO
// =======================
export async function getMe(token: string) {
  const response = await axios.get(`${API_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
}
