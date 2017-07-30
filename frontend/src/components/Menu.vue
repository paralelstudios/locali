<template>
  <section id="menuOptions">
    <router-link v-for="option in menuOptions" :to="option.target" :key="option.id">
      <choice :target="option.target" :label="option.name"></choice></router-link>
  </section>
</template>


<script>

import Choice from "./Choice.vue";

export default {
    name: "menu",
    components: {
	Choice
    },
    data () {
	return {
	    menuOptions: [
		{name: "Practice", id: "a", target: "practice"},
		{name: "Places", id: "b", target: "places"},
		{name: "Plants", id: "c", target: "plants"},
		{name: "In Season", id: "d", target: "season"}
	    ]
	};
    },
}
</script>

<style scoped>

#menuOptions {
    justify-content: space-around;
    align-items: center;
}

#menuOptions a {
    text-decoration: none;
}

#menuOptions .choice {
    font-size: 7vh;
    font-weight: 300;
    height: 15vh;
    width: 85vw;
}
#menuOptions .choice:hover {
    background-color: #1B7F20;
    margin-top: 3vh;
    margin-bottom: 1vh;
}

</style>
