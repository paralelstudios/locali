<template>
  <div id="multiple-choice"><choice v-for="choice in choices" :label="choice.name" :target="choice.target" :key="choice.id" @submit="checkChoice"></choice></div>
</template>

<script>
import Choice from "./Choice.vue"

export default {
    name: "multiple-choice",
    components: {
	Choice
    },
    methods: {
	checkChoice (choiceEl) {
	    if (choiceEl.option !== this.correctChoice) {
 		choiceEl.$el.disabled = true;
		return;
	    }

	    this.$emit("correct");
	}
    }
}

</script>
