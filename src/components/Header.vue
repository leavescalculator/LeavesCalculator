<template>
  <ul class="nav nav-tabs">
    <router-link
      to="/"
      class="nav-item nav-link"
      tag="li"
      active-class="active"
      exact
    >
      <a v-if="username === ''">Login</a>
      <a v-else>Log out</a>
    </router-link>
    <router-link
      to="/questions"
      class="nav-item nav-link"
      tag="li"
      active-class="active"
    >
      <a>Questions</a>
    </router-link>
    <router-link
      to="/report"
      class="nav-item nav-link"
      tag="li"
      active-class="active"
    >
      <a>Report</a>
    </router-link>
    <router-link
      to="/admin-dashboard"
      class="nav-item nav-link"
      tag="li"
      active-class="active"
      v-if="isAdmin"
    >
      <a>Admin</a>
    </router-link>
    <router-link
      to="/graph-dashboard"
      class="nav-item nav-link"
      tag="li"
      active-class="active"
      v-if="isAdmin"
    >
      <a>Graphs</a>
    </router-link>
    <router-link
      to="/report-dashboard"
      class="nav-item nav-link"
      tag="li"
      active-class="active"
    >
      <a>Past Reports</a>
    </router-link>
  </ul>
</template>

<script>
export default {
  name: "Header",
  props: ["username", "isAdmin"]
};
</script>

<style scoped></style>
