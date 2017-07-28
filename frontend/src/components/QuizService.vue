<template>
  <div id="quiz">
    <quiz-entity :imageUrl="imageUrl"></quiz-entity>
    <section id="control-panel">
      <user-message v-if="userMessage" :message="userMessage"></user-message>
      <user-message v-else-if="loading" :message="loadingMessage"></user-message>
      <multiple-choice v-else :choices="choices" :correctChoice="name" @correct="setNewEntity"></multiple-choice>
  </section></div>

</template>

<script>

import QuizEntity from "./QuizEntity.vue";
import MultipleChoice from "./MultipleChoice.vue";
import UserMessage from "./UserMessage.vue";
import config from "../config";
import sampleSize from 'lodash.samplesize';
import shuffle from 'lodash.shuffle';

export default {
    data () {
	return {
 	    quiz: "plants",
	    item: {},
	    choices: [],
	    solved: [],
	    loading: false,
	    loadingMessage: {text: "Loading..."},
	    userMessage: null
	};
    },
    computed: {
	imageUrl () { return this.item["image_url"]; },
	name () { return this.item["name"]; }
    },
    components: {
	QuizEntity,
	MultipleChoice,
	UserMessage
    },
    created () { this.getItems(); },
    methods: {
	getItems () {
	    var vm = this;
	    this.$http.get("/api/quizzes/" + this.quiz)
		.then(function (resp) {
		    vm.items = shuffle(resp.data);
		    vm.downloadImage(
			vm.items[0],
			function () {
			    vm.loading = false;
			    vm.setEntity();
			}
		    );
		})
		.catch(function (err) {
 		    vm.userMessage = {isError: true,
				      text: err.response.data.description ||
				      err.response.statusText};
		});
	},
	setNewEntity () {
	    this.solved.push(this.item);
	    if (!this.items.length) {
		this.win();
		return;
	    }
	    this.setEntity();
	},
	setEntity (item) {
	    this.userMessage = null;
	    this.item = this.items.shift();
	    this.choices = this._getOptions();
	    if (this.items.length) {
		this.loading = true;
		this.downloadImage(this.items[0]);
		this.items.slice(
		    1,
		    (this.items.length - 1) < 2 ? this.items.length : 2
		).map(this.downloadImage);
	    }
	},
	downloadImage (item, onload) {
	    var img = new Image(),
		vm = this;
	    img.onload = function () {
		vm.loading = false;
		if (onload) { onload(); }
	    };
	    img.src = item["image_url"];
	},
	win () {
	    this.userMessage = {text: "You won!\nRefresh to replay"};
	    this.item = {name: "Para-lel Studios", image_url: "resources/imgs/paralel-logo.png"};
	    this.choices = [];
	},
	_getOptions () {
	    var options = shuffle(["a", "b", "c", "d"]),
		choices = sampleSize(
		shuffle(this.items.concat(this.solved)),
		3
	    ).concat(
		[this.item]
	    );
	    console.log("choices", choices)
	    return choices.map(function (el) {
		return {name: el["name"], target: el["name"], id: options.pop()};
	    });
	}
    }
}
</script>
