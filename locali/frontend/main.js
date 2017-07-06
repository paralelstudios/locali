var host = 'http://127.0.0.1:5000';
var instance = axios.create({
    baseURL: host });

Vue.component('user-message', {
    props: ["message"],
    template: '<div class="choice message" :class="{error: message.isError}">{{ message.text }}</div>'
});

Vue.component('choice', {
    props: ['label', "target"],
    template: '<button :id="$vnode.key" :value="target" @click="submitChoice" class="choice"><span>{{ label }}</span></button>',
    computed: {
	option: function () {
	    return this.label.trim().toLowerCase();
	}
    },
    methods: {
	submitChoice: function () {
	    this.$emit("submit", this);
	}
    }
});

var Menu = {
    data: function () {
	return {
	    menuOptions: [
		{name: "Practice", id: "a", target: "quiz"},
		{name: "Places", id: "b", target: "places"},
		{name: "Plants", id: "c", target: "plants"},
		{name: "In Season", id: "d", target: "season"}
	    ]
	};
    },
    template: '<div id="menuOptions"><choice v-for="option in this.menuOptions" :label="option.name" :target="option.target" :key="option.id" @submit="changeView">' +
	'</choice></div>',
    methods: {
	changeView: function (choice) {
	    this.$emit("change-view", choice.target);
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
    template: '<div id="multiple-choice"><choice v-for="choice in choices" :label="choice.name" :target="choice.target" :key="choice.id" @submit="checkChoice"></choice></div>',
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
	}
    },
    components: {
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
		return {name: el["name"], target: el["name"], id: options.pop()};
	    });
	}
    }

};

var NYI = {
    data: function () {
	return {
	    userMessage: {text: "Nothing here yet!"}
	};
    },
    template: '<user-message :message="userMessage"></user-message>'
};

var app = new Vue({
    el: "#app",
    data: {
	currentView: 'mainMenu'
    },
    components: {
	quiz: Quiz,
	season: NYI,
	plants: NYI,
	places: NYI,
	mainMenu: Menu
    },
    created: function () {
	document.getElementById("init").style.display = "none";
    },
    methods: {
	changeView: function (view) {
	    this.currentView = view;
	}
    }
});
