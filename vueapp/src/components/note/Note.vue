<template>
  <v-container>
    <v-card v-for="item in notes" :style="{'margin': '5px'}">
      <v-card-text>
        <div>{{ item.text }}</div>
      </v-card-text>
      <v-img v-if="item.image" :src="item.image"></v-img>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: 'Note',
    data: function () {
      return {
        notes: null
      }
    },
    mounted() {
        this.getNotes()
    },
    methods: {
      getNotes() {
            let user = JSON.parse(sessionStorage.getItem('user'));
            let headers = user ? {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${user.access}`,
            } : {};
            this.axios.get(`${this.$apiHost}/api/v1/note/`, {
              headers: headers
            }).then((result) =>{
              console.log(result.data)
              this.notes = result.data;
        }).catch((res) => {
            sessionStorage.removeItem('user');
            this.$router.push('login');
        })
      }
    }
  }
</script>
