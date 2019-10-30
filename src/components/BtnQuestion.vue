<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
        <button class="btn btn-success" v-for="(option, index) in options" :key='index'
            @click="selected(index)">{{ option.title }}</button>
    </div>
</template>

<script>
export default {
    data: () => ({

    }),
    props: ['title', 'options'],
    methods: {
        selected (index) {
            this.$emit('option-selected', index);
        }
    }
        
    
}
</script>
<style scoped>
    .btn {
        margin-right: 5px;
    }
</style>