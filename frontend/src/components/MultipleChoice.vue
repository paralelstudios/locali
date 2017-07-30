<template>
  <div id="multiple-choice"><choice v-for="choice in choices" :label="choice.name" :target="choice.target" :key="choice.id" @submit="checkChoice"></choice></div>
</template>

<script>
import Choice from "./Choice.vue"

export default {
    name: "multiple-choice",
    props: ["choices", "correctChoice"],
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

<style scoped>
#multiple-choice {
    display: grid;
    height: 100%;
    width: 100%;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
}
#multiple-choice .choice {
    transition: all .2s ease;
}
#multiple-choice .choice > span {
    font-size: 5vw;
    letter-spacing: 0.5vw;
}


#a.choice {
    grid-column: 1;
    grid-row: 1;
}

#b.choice {
    grid-column: 2;
    grid-row: 1;
}

#c.choice {
    grid-column: 1;
    grid-row: 2;
}

#d.choice {
    grid-column: 2;
    grid-row: 2;
}

</style>
