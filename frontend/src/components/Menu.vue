<template>
  <section id="menuOptions">
    <router-link v-for="option in this.menuOptions" :to="option.target" :key="option.id">
      <choice :target="option.target" :label="option.name" @submit="changeView"></choice>
    </router-link>
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
    methods: {
	changeView (choice) { this.$emit("change-view", choice.target); }
    }
}
</script>
