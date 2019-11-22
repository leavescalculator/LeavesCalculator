<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
      <p> {{ description }}</p>
    </div>
</template>

<script>
export default {
    data: () => ({

    }),
    props: ['title', 'options', 'description'],
    methods: {}


}
</script>
<style scoped>
    .btn {
        margin-right: 5px;
    }
</style>
