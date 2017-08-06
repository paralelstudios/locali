<template>
  <menu id="profileMenu">
    <li v-if="$store.state.loggedIn"><router-link to="/profile"><button>profile</button></router-link></li>
    <li v-if="$store.state.loggedIn"><button @click="logout">logout</button></li>
    <li v-if="!$store.state.loggedIn"><router-link to="/login"><button>login/register</button></router-link></li>
  </menu>
</template>

<script>

export default {
    name: "profile-menu",
    methods: {
	logout () {
	    this.$store.commit("LOGOUT")
	    this.$router.push("/menu")
	},
	ensureLogin () {
	    if (!this.$store.state.loggedIn) {
		this.$router.push("/login")
	    }
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
