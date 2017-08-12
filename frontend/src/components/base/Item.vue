<template>
  <section class="elementView">
    <article>
      <user-message v-if="userMessage" :message="userMessage"></user-message>
      <slot>
	<h2>{{ item.primary_name }}</h2><hr>
	<img :src="item.photo" :alt="item.name"/>
	<p>{{ item.description }}</p>
      </slot>
    </article>
  </section>

</template>
<script>


import UserMessage from "./UserMessage.vue";

export default {
    data () {
	return {
	    userMessage: null,
	    item_name: null,
	    endpoint: null,
	    item: {primary_name: "",
		   photo: "resources/imgs/paralel-logo.png",
		   description: ""}
	};
    },
    created () {
	this.getItem();
    },
    components: {
	UserMessage
    },
    methods: {
	getItem () {
	    var vm = this;
	    this.$http.get("/api" + this.endpoint + "/" + this.$route.params.name)
		.then((resp) => {
		    vm.item = resp.data;
		})
		.catch((err) => {
		    vm.userMessage = {isError: true,
				      text: err.response.data.description ||
				      err.response.statusText};
		});
	}
    }

};
</script>
