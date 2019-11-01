<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
        <select class="select-picker" v-model="selectedIndex" style="width: 50em;">
          <option :value="index" v-for="(option, index) in options" :key="index">{{ option.title }}</option>
        </select>
        <br>
        <button @click="selected(selectedIndex)">Next</button>
        <br>
        {{ selectedIndex }}
    </div>
</template>

<script>
export default {
    data: () => ({
      selectedIndex: 0,
    }),
    props: ['title', 'options'],
    methods: {
      selected (index) {
        console.log(index)
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