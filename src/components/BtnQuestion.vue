<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
      <div class="row">
        <button class="btn btn-success col" v-for="(option, index) in options" :key='index'
                @click="selected(index)">{{ option.title }}</button>
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
