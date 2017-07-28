import VueRouter from 'vue-router';
import QuizService from "./components/QuizService.vue";
import Menu from "./components/Menu.vue";
import { Element, List, Item, PlaceItem } from "./helpers";


const router = new VueRouter({
    mode: process.env.NODE_ENV === "production" ? 'history': '',
    routes: [
	{path: "/season",
	 name: "season",
	 component: List("plants", "plant", "/season")},
	{path: "/places",
	 name: "places",
	 component: List("places", "place", "/places")},
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
	{path: "*", name: "menu", component: Menu},
    ]
});


export default router;
