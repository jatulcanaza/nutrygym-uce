import axios from "axios";

const API_URL = "http://localhost:3001";

// =======================
// LOGIN
// =======================
export async function loginUser(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email); // FastAPI usa username
  formData.append("password", password);

  const response = await axios.post(
    `${API_URL}/auth/login`,
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
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
// LOGOUT
// =======================
export async function logoutUser(token: string) {
  const response = await axios.post(
    `${API_URL}/auth/logout`,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return response.data;
}
