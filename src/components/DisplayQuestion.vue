<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
        <p v-for="(option, index) in options" :key="index"> {{option.title }}</p>
        display
    </div>
</template>

<script>
export default {
    data: () => ({

    }),
    props: ['title', 'options'],
    methods: {
    
    }
        
    
}
</script>
<style scoped>
    .btn {
        margin-right: 5px;
    }
</style>