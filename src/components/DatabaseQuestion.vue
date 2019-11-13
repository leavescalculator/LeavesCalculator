<template>
    <div class="">
        <h2>{{ title }}</h2>
        <hr>
        database
    </div>
</template>

<script>
export default {
    data: () => ({
    }),
    props: ['title', 'options', 'user'],
    methods: {
        //Assumes the option.title of any db node is structured in a specific way
        //"OPP prop value" ie "== fmla_eligibility T"
        parse(str) {
            let args = str.split(' ');
            switch (args[0]) {
                case '==':
                    if (this.user.hasOwnProperty(args[1]))
                    {
                        return this.user[args[1]] === args[2];
                    }
                    break;
                case '<':
                    if (this.user.hasOwnProperty(args[1]))
                    {
                        return this.user[args[1]] < args[2];
                    }
                    break;
                case '>=':
                    if (this.user.hasOwnProperty(args[1]))
                    {
                        return this.user[args[1]] >= args[2];
                    }
                    break;
                case 'else':
                    return true;
                default:
                    return false;

            }
            return false;
        }
    },
    mounted() {
      console.log("Options: " + this.options.length);
        let i = 0;
      while (i < this.options.length) {
          console.log(i);
          if (this.options[i].hasOwnProperty('title')) {
              if (this.parse(this.options[i].title)) {
                  this.$emit('option-selected', i);
                  console.log("Selected " + i);
                  return;
              }
          }
          i++;
      }
    }


}
</script>
<style scoped>
    .btn {
        margin-right: 5px;
    }
</style>
