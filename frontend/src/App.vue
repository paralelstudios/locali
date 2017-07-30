<template>
  <main id="app">
    <app-header></app-header>
    <router-view></router-view>
  </main>
</template>

<script>

import store from "./store"
import router from "./router"
import AppHeader from "./components/Header.vue"
import config from "./config"

export default {
    name: 'app',
    router,
    store,
    components: {
	AppHeader
    },
}
</script>
