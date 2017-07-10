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
		{name: "Practice", id: "a", target: "practice"},
		{name: "Places", id: "b", target: "places"},
		{name: "Plants", id: "c", target: "plants"},
		{name: "In Season", id: "d", target: "season"}
	    ]
	};
    },
    template: '<div id="menuOptions"><router-link v-for="option in this.menuOptions" :to="option.target" :key="option.id"><choice :target="option.target" :label="option.name" @submit="changeView">' +
	'</choice></router-link></div>',
    methods: {
	changeView: function (choice) {
	    this.$emit("change-view", choice.target);
	}
    }}
;

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

var QuizService = {
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

var FourOFour = {
    data: function () {
	return {
	    userMessage: {text: "Where do you think you are, man?"}
	};
    },
    template: '<user-message :message="userMessage"></user-message>'
};


function Element (element) {
    return {
	props: [element],
	template: '<button class="' + element + 'Element" :value="' + element + '.name" @click="select">' +
	    '<h4 class="' + element + 'Name">{{ ' + element + '.name }}</h4>' +
	    '<p class="' + element + 'Description">{{ ' + element + '.description }}</p>' +
	    '</button>',
	methods: {
	    select: function () {
		this.$emit("select", this[element]);
	    }
	}
    };
};

function List(items, item, endpoint, parameter) {
    return {
	data: function () {
	    return {
		items: [{name: "Test " + item,
			      description: "This is a test " + item}],
		selectedItem: null
	    };
	},
	computed: {
	    parameter: function () {
		return parameter ? "/" + parameter + "/" + this.$route.params.name : "";
	    }
	},
	components: {
	    itemElement: Element(item)
	},
	template: '<section id="categories"">' +
	    '<item-element v-for="item in items" :key="item.name" :' + item + '="item" @select="select"></item-element>' +
	    '</section>',
	created: function () {
	    console.log("Creating "  + items + " List");
	    this.getItems();
	},
	methods: {
	    select: function (selectedItem) {
		this.$router.push(
		    {name: item,
		     params: {
			 name: selectedItem.name.toLowerCase().replace(" ", "_")
		     }}
		);
	    },
	    getItems: function () {
		var vm = this;
		instance.get(endpoint + this.parameter)
		    .then(function (resp) {
			vm.items = resp.data;
		    })
		    .catch(function (err) {
			console.log(err);
 			vm.userMessage = {isError: true, text: err.message };
		    });
	    }
	}
    };
};


function Item (item, endpoint) {
    return  {
	data: function () {
	    return {
		item: {name: "Test " + item,
			photo: "resources/imgs/paralel-logo.png",
			description: "blah blah"}
	    };
	},
	created: function () {
	    console.log("Creating " + item + " page");
	    this.getItem();
	},
	template: '<article class=' + item + '>' +
	    '<h2 class="' + item + 'Title">{{ item.name }}</h2><hr>' +
	    '<img class="' + item + 'Photo" :src="item.photo" :alt="item.name"/>' +
	    '<p class="' + item + 'Description">{{ item.description }}</p>' +
	    '</article>',
	methods: {
	    getItem: function() {
		var vm = this;
		instance.get(endpoint + "/" + this.$route.params.name)
		    .then(function (resp) {
			vm.item = resp.data;
		    })
		    .catch(function (err) {
			console.log(err);
 			vm.userMessage = {isError: true, text: err.message };
		    });
	    }
	}

    };
}

function PlaceItem () {
    var item = Item("place", "/places");
    item.data = function () {
	return {
	    item: {name: "Test place",
		   primary_image: "resources/imgs/paralel-logo.png",
		   description: "blah blah",
		   plants: [{name: "plant1"},
			    {name: "plant2"}]}};

    };
    if (item.components) {
	item.components["itemElement"] = Element("plant");
    } else {
	item.components = {itemElement: Element("plant")};
    }
    item.methods.select = function (plant) {
	this.$router.push(
	    {name: 'plant',
	     params: {
		 name: plant.name.toLowerCase().replace(" ", "_")
	     }}
	);
    };
    item.template = '<article class="place">' +
	'<h2 class="placeTitle">{{ item.name }}</h2><hr>' +
	'<img class="placePhoto" :src="item.primary_image" :alt="item.name"/>' +
	'<p class="placeDescription">{{ item.description }}</p>' +
	'<hr><h4>Plants</h4><hr>' +
	'<menu><item-element v-for="plant in item.plants" :key="plant.name" :plant="plant" @select="select"></item-element></menu>' +
	'</article>';
    return item;
};


var router = new VueRouter({
//    mode: 'history',
    routes: [
	{path: "/season",
	 name: "season",
	 component: List("plants", "plant", "/season")},
	{path: "/places",
	 name: "places",
	 component: List("categories", "category", "/places/categories")},
	{path: "/practice",
	 name: "practice",
	 component: QuizService},
	{path: "/plants",
	 name: "plants",
	 component: List("plants", "plant", "/plants")},
	{path: "/places/:name",
	 name: "place",
	 component: PlaceItem()},
	{path: "/plants/:name",
	 name: "plant",
	 component: Item("plant", "/plants")},
	{path: "/places/categories/:name",
	 name: "category",
	 component: List("places", "place", "/places", "category")},
	{path: "*", name: "menu", component: Menu},
    ]
});

var app = new Vue({
    el: "#app",
    router: router,
    methods: {
	updateHeader: function () {
	    var header = this.$route.name;
	    if (header !== "menu") {
		header = "menu" + " > " + this.$route.name.replace("_", " ");
	    }
	    document.getElementById("header").text = header;
	}
    },
    created: function () {
	document.getElementById("init").style.display = "none";
	this.updateHeader();
    },
    watch: {
	'$route': function (to, from) {
	    this.updateHeader();
	}
    }
});
