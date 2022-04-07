export default {
    methods: {
        getHeaders() {
            let user = JSON.parse(sessionStorage.getItem('user'));
            let headers = user ? {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user.access}`,
            } : {};
            return headers;
        },
        dropSession() {
            sessionStorage.removeItem('user');
            this.$router.push('login');
        },
    }
}