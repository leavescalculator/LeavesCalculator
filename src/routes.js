import Login from "./components/Login";
import Questions from "./components/Questions";
import Report from "./components/Report";

export const routes = [
//route for the home route of the web page
  { path: '/', component: Login },
  { path: '/questions', component: Questions },
  { path: '/report', component: Report }
];
