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

var NYI = {
    data: function () {
	return {
	    userMessage: {text: "Nothing here yet!"}
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
	props: parameter ? [parameter] : [],
	data: function () {
	    return {
		items: [{name: "Test " + item,
			      description: "This is a test " + item}],
		selectedItem: null
	    };
	},
	computed: {
	    parameter: function () {
		return parameter ? "/" + parameter + "/" +
		    this.$props[parameter]
		    .toLowerCase()
		    .split(" ")
		    .join("_") : "";
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
		this.$emit("view-" + item, selectedItem.name);
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
	props: [item],
	data: function () {
	    return {
		item: {name: "Test " + item,
			photo: "resources/imgs/paralel-logo.png",
			description: "blah blah"}
	    };
	},
	computed: {
	    parameter: function () {
		return "/" +
		    this.$props[item]
		    .toLowerCase()
		    .split(" ")
		    .join("_");
	    }
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
		instance.get(endpoint + this.parameter)
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

var SeasonService = {
    data: function () {
	return {
	    currentView: "season",
	    plant: null
	};
    },
    components: {
	season: List("plants", "plant", "/season"),
	plant: Item("plant", "/plants")
    },
    template: '<section id="season">' +
	'<component :plant="plant" :is="currentView" @view-plant="viewPlant"></component>' +
	'</section>',
    methods: {
	viewPlant: function (plant) {
	    this.plant = plant;
	    this.currentView = 'plant';
	}
    }
};

var PlantService = {
    data: function () {
	return {
	    plant: null,
	    currentView: "plants"
	};
    },
    components: {
	plants: List("plants", "plant", "/plants"),
	plant: Item("plant", "/plants")
    },
    template: '<section id="plants">' +
	'<component :plant="plant" :is="currentView" @view-plant="viewPlant"></component>' +
	'</section>',
    methods: {
	viewPlant: function (plant) {
	    this.plant = plant;
	    this.currentView = "plant";
	}
    }
};

var PlaceService = {
    data: function () {
	return {
	    currentView: 'categories',
	    category: null,
	    place: null
	};
    },
    components: {
	categories: List("categories", "category", "/places/categories"),
	categoryPlaces: List("places", "place", "/places", "category"),
	place: Item("place", "/places")
    },
    template: '<section id="places">' +
	'<component :place="place" :category="category" :is="currentView" @view-category="viewCategory" @view-place="viewPlace"></component>' +
	'</section>',
    methods: {
	viewCategory: function (category) {
	    this.category = category;
	    this.currentView = "categoryPlaces";
	},
	viewPlace: function (place) {
	    this.place = place;
	    this.currentView = "place";
	}
    }
};

var app = new Vue({
    el: "#app",
    data: {
	currentView: 'main menu'
    },
    components: {
	quiz: QuizService,
	season: SeasonService,
	plants: PlantService,
	places: PlaceService,
	"main menu": Menu
    },
    created: function () {
	document.getElementById("init").style.display = "none";
	document.getElementById("header").text = this.currentView;
    },
    methods: {
	changeView: function (view) {
	    this.currentView = view;
	    document.getElementById("header").text = this.currentView;
	}
    }
});
