import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);
export default new Vuex.Store({
    strict: process.env.NODE_ENV !== 'production',
    state: {
	loggedIn: !!localStorage.getItem('access_token'),
	email: localStorage.getItem("email")
    },
    mutations: {
	LOGIN (state, payload) {
	    localStorage.setItem("access_token", payload.access_token)
	    localStorage.setItem("email", payload.email)
	    state.loggedIn = true
	    state.email = payload.email
	},
	LOGOUT (state) {
	    localStorage.removeItem("access_token")
	    localStorage.removeItem("email")

	    state.loggedIn = false
	    state.email = null
	}
    }
});
