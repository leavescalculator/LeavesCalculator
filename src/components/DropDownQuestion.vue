<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
        <select class="select-picker">
          <option :value="option" v-for="option in options" :key="option">{{ option.title }}</option>
        </select>
        drop down
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