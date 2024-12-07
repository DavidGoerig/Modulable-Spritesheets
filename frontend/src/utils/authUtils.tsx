export const isAuthenticated = (): boolean => {
    const token = localStorage.getItem('token');
    // Add your token validation logic here if needed
    return !!token;
};