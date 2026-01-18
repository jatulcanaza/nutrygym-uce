import React, { createContext, useContext, useEffect, useState } from "react";
import { getMe } from "../api/auth.api";
import { getMyRole, type Role } from "../api/authorization.api";

interface User {
  email: string;
}

interface AuthContextType {
  token: string | null;
  user: User | null;
  role: Role | null;
  isLoadingRole: boolean;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [user, setUser] = useState<User | null>(null);

  const [role, setRole] = useState<Role | null>(null);
  const [isLoadingRole, setIsLoadingRole] = useState(false);

  useEffect(() => {
    if (!token) {
      setUser(null);
      return;
    }

    getMe(token)
      .then(setUser)
      .catch(() => logout());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  useEffect(() => {
    if (!token) {
      setRole(null);
      setIsLoadingRole(false);
      return;
    }

    setIsLoadingRole(true);

    getMyRole(token)
      .then((r) => setRole(r))
      .catch((err) => {
        console.error("getMyRole failed:", err?.response?.data || err?.message || err);
        setRole(null);
      })
      .finally(() => setIsLoadingRole(false));
  }, [token]);

  const login = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    setRole(null);
    setIsLoadingRole(false);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        role,
        isLoadingRole,
        isAuthenticated: !!token,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
