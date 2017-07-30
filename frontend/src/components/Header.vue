<template>
  <header>
    <router-link to="/info"><info-button></info-button></router-link>
    <router-link id="routeName" to="/menu"><h1 @mouseenter="mouseenterRouteName" @mouseleave="mouseleaveRouteName">{{ mouseOverRouteName ? "menu" : routeName }}</h1></router-link>
    <profile-button @click.native="menuShldBeOpen = !menuShldBeOpen" ></profile-button>
    <profile-menu @click.native="menuShldBeOpen = false" v-if="menuShldBeOpen"></profile-menu>
  </header>
</template>

<script>

import ProfileButton from "./ProfileButton.vue"
import InfoButton from "./InfoButton.vue"
import ProfileMenu from "./ProfileMenu.vue"

export default {
    name: "app-header",
    data () {
	return { mouseOverRouteName: false, menuShldBeOpen: false };
    },
    components: {
	ProfileButton,
	InfoButton,
	ProfileMenu
    },
    computed: {
	routeName () {
	    return this.$route.name.replace("-", " ");
	}
    },
    methods: {
        mouseenterRouteName () { this.mouseOverRouteName = true; },
	mouseleaveRouteName () { this.mouseOverRouteName = false; },
	toggleMenu () { console.log("click"); this.menuShldBeOpen = !this.menuShldBeOpen; },
   }
}
</script>
