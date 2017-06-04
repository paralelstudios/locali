var host = 'http://127.0.0.1:5000';
var instance = axios.create({
    baseURL: host });

var UserMessage = {
    props: ["message"],
    template: '<div class="choice message" :class="{error: message.isError}">{{ message.text }}</div>'

};

var Choice = {
    props: ['value'],
    template: '<option :id="$vnode.key" :value="value" @click="submitChoice" class="choice"><span>{{ value }} </span></option>',
    computed: {
	option: function () {
	    return this.value.trim().toLowerCase();
	}
    },
    methods: {
	submitChoice: function () {
	    this.$emit("submit", this);
	}
    }
};

var QuizEntity = {
    props: ["imageUrl"],
    template: '<section id="entity">' +
	'<img name="entityImg" :src="imageUrl">' +
	'</section>'
};

var MultipleChoice = {
    props: ["choices", "correctChoice"],
    template: '<datalist id="multiple-choice"><choice v-for="choice in choices" :value="choice.name" :key="choice.id" @submit="checkChoice"></choice></datalist>',
    components: {
	'choice': Choice
    },
    methods: {
    	checkChoice: function (choiceEl) {
	    if (choiceEl.option !== this.correctChoice) {
		choiceEl.$el.disabled = true;
		return;
	    }

	    this.$emit("correct");
	}
    }
};

var Quiz = {
    data: function () {
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
	imageUrl: function () {
	    return this.item["image_url"];
	},
	name: function () {
	    return this.item["name"];
	},
    },
    components: {
	'user-message': UserMessage,
	'quiz-entity': QuizEntity,
	'multiple-choice': MultipleChoice
    },
    template: '<div id="quiz">' +
	'<quiz-entity :imageUrl="imageUrl"></quiz-entity>' +
	'<section id="control-panel">' +
	'<user-message v-if="userMessage" :message="userMessage"></user-message>' +
	'<user-message v-else-if="loading" :message="loadingMessage"></user-message>' +
	'<multiple-choice v-else :choices="choices" :correctChoice="name" @correct="setNewEntity"></multiple-choice>' +
	'</section></div>',

    created: function () {
	this.getItems();
    },
    methods: {
	getItems: function () {
	    var vm = this;
	    instance.get("/quizzes/" + this.quiz)
		.then(function (resp) {
		    vm.items = _.shuffle(resp.data);
		    vm.downloadImage(
			vm.items[0],
			function () {
			    vm.loading = false;
			    vm.$emit("ready");
			    vm.setEntity();
			}
		    );
		})
		.catch(function (err) {
		    console.log(err);
 		    vm.userMessage = {isError: true, text: err.message };
		});
	},
	setNewEntity: function () {
	    this.solved.push(this.item);
	    if (!this.items.length) {
		this.win();
		return;
	    }
	    this.setEntity();
	},
	setEntity: function (item) {
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
	downloadImage: function (item, onload) {
	    var img = new Image(),
		vm = this;
	    img.onload = function () {
		vm.loading = false;
		if (onload) { onload(); }
	    };
	    img.src = item["image_url"];
	},
	win: function () {
	    this.userMessage = {text: "You won!\nRefresh to replay"};
	    this.item = this.default_item;
	    this.choices = [];
	},
	_getOptions: function () {
	    var options = _.shuffle(["a", "b", "c", "d"]),
		choices = _.sampleSize(
		_.shuffle(this.items.concat(this.solved)),
		3
	    ).concat(
		[this.item]
	    );
	    return choices.map(function (el) {
		return {name: el["name"], id: options.pop()};
	    });
	},
    }

};

var ItemUpload = {
    template: '<form method=POST enctype=multipart/form-data>' +
	'<input type=file name=photo>' +
	'</form>'
}

var app = new Vue({
    el: "#app",
    data: {
	currentView: 'quiz'
    },
    components: {
	quiz: Quiz
    },
    methods: {
	removeInit: function () {
	    document.getElementById("init").style.display = "none";
	}
    }
});
