<template>
  <section class="elementList">
    <user-message v-if="userMessage" :message="userMessage"></user-message>
    <item-element :element="item" v-else v-for="item in items" :key="item.name" @select="select"><p>{{ item.description }} </p></item-element>
    <add-button v-if="$store.state.loggedIn" @add="add"></add-button>
    </section>
</template>

<script>

import Element from "./Element.vue"
import AddButton from "./AddButton.vue"
import UserMessage from "./UserMessage.vue"

export default {
    name: "list",
    data () {
	return {
	    userMessage: null,
	    items: [],
	    selectedItem: null
	};
    },
    props: ["endpoint", "name", "select_route"],
    components: {
	itemElement: Element,
	UserMessage,
	AddButton
    },
    created () {
	this.getItems();
    },
    methods: {
	add () { this.$router.push("/add/" + this.name ); },
	select (selectedItem) {
	    this.$router.push(
		{name: this.select_route,
		 params: {
		     name: selectedItem.name.toLowerCase().replace(" ", "_")
		 }}
	    );
	},
	getItems () {
	    var vm = this;
	    this.$http.get("/api" + this.endpoint)
		.then(function (resp) {
		    vm.items = resp.data;
		})
		.catch(function (err) {
		    vm.userMessage = {isError: true,
				      text: err.response.data.description ||
				      err.response.statusText};
		});
	}
    }
};

</script>

<style>
</style>
