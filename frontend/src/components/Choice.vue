<template>
  <button :id="$vnode.key" :value="target" @click="submitChoice" class="choice"><slot><span>{{ label }}</span></slot></button>
</template>

<script>
    export default {
	name: "choice",
	props: ["label", "target"],
	computed: {
	    option () {
		return this.label.trim().toLowerCase();
	    }
	},
	methods: {
	    submitChoice () { this.$emit("submit", this); }
	}
    }
</script>

<style scoped>
.choice {
    letter-spacing: 1vw;
    border-radius: 10px;
    font-size: 3vh;
    margin: .5vh;
    text-align: center;
    background-color: #43A047;
    box-shadow: 0px 0px 15px -5px black;
    text-transform: capitalize;
    transition: all .5s ease;
}
.choice:enabled:hover {
    background-color: #2E7D32;
}

@keyframes vibrate {
    0% {margin-left: 0px;}
    25% {margin-right: 5px;}
    50% {margin-right: 0px;}
    75% {margin-left: 5px;}
    100% {margin-left: 0px;}
}

.choice:disabled {
    opacity: 0.5;
    animation: .1s linear 0s 3 vibrate;
    background-color: #F44336;

}
.choice:active:hover {
    background-color: #1B7F20;
}
.choice {
    box-shadow: 0px 0px 5px -10px rgba(0, 0, 0, 0.4);
}

</style>
