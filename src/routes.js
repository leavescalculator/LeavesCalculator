import Login from "./components/Login";
import Questions from "./components/Questions";
import Report from "./components/Report";
import AdminDashboard from "./components/AdminDashboard";
import GraphsDashboard from "./components/GraphsDashboard";

export const routes = [
  //route for the home route of the web page
  { path: "/", component: Login },
  { path: "/questions", component: Questions },
  { path: "/report", component: Report },
  { path: "/admin-dashboard", component: AdminDashboard },
  { path: "/graph-dashboard", component: GraphsDashboard }
];
