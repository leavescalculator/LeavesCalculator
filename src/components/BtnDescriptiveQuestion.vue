<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
        <div v-for="(option, index) in options" :key='index' class="row">
            <button class="btn btn-success col col-md-2" @click="selected(index)">{{ option.title }}</button>
          <p class="col">{{ option.description }}</p>
        </div>

    </div>
</template>

<script>
export default {
    data: () => ({

    }),
    props: ['title', 'options'],
    methods: {
        selected (index) {
            console.log(index)
            this.$emit('option-selected', index);
        },
    }
}
</script>
<style scoped>
    .btn {
        margin-right: 5px;
    }
</style>
