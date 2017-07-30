<template>
  <menu id="profileMenu">
    <li v-if="loggedIn"><router-link to="/profile"><button>profile</button></router-link></li>
    <li v-if="loggedIn"><button @click="logout">logout</button></li>
    <li v-if="!loggedIn"><router-link to="/login"><button>login</button></router-link></li>
  </menu>
</template>

<script>

import store from "../store"
import router from "../router"

export default {
    name: "profile-menu",
    computed: {
	loggedIn () { return store.state.loggedIn; }
    },
    methods: {
	logout () {
	    store.commit("LOGOUT")
	    router.push("/menu")
	},
	ensureLogin () {
	    if (!store.state.loggedIn) {
		router.push("/login")
	    }
	},
	click () {
	    this.ensureLogin()
	    this.menuIsOpen = !this.menuIsOpen
	},
	openMenu () {
	    this.menuIsOpen = true;
	},
	closeMenu () {
	    this.menuIsOpen = false;
	}

    }
}


</script>

<style scoped>
#profileMenu {
    position: absolute;
    right: 0;
    top: 12.5vh;
    z-index: 1000;
}
#profileMenu > li {
    display: flex;
    justify-content: center;

}
#profileMenu {
    background-color: #F1F8E9;
    box-shadow: 0px 5px 15px -5px black;
}
#profileMenu *{
    background-color: #F1F8E9;
}
#profileMenu button {
    font-size: 5vh;
    color: #33691E;
    transition: all 0.5s ease;
    padding: 0 5vw;
}
#profileMenu button:hover {
    background-color: #C8E6C9;
}
</style>
