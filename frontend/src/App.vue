<template>
  <main id="app">
    <header><a id="header" href="/"><h1>{{ header }}</h1></a></header>
    <router-view></router-view>
  </main>
</template>

<script>
import router from "./router"
import config from "./config"

export default {
    name: 'app',
    router: router,
    computed: {
	header () {
	    return this.$route.name.replace("-", " ");
	}
    }
}
</script>
