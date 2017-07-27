<template>
  <user-message :message="userMessage"></user-message>
</template>

<script>

import UserMessage from "./UserMessage";

export default {
    data () {
	return {
	    userMessage: {text: "Where do you think you are, man?"}
	}
    }
}
</script>
