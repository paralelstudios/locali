<template>
  <button :id="$vnode.key" :value="target" @click="submitChoice" class="choice"><span>{{ label }}</span></button>
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
