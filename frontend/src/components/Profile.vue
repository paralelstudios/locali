<template>
  <section class="elementView" id="profile">
    <article>
      <h2>Profile</h2>
      <hr>
      <p>You're a dipshit</p>
    </article>
  </section>
</template>

<script>

import store from "../store"
import router from "../router"

export default {
    name: "profile",
    beforeCreate () {
        if (!store.state.loggedIn) {
            router.push('/login')
        }
    },
    data () {
	return {
	}
    },
}

</script>


<style scoped>
#profileBtn {
    margin-top: 2vh;
    font-size: 5vh;
}
</style>
