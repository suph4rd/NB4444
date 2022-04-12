<template>
  <v-container>
    <NoteCreate :style="{'margin-bottom': '70px'}" @onCreate="getNotes" />

    <v-text-field
      v-if="!notes"
      color="success"
      loading
      disabled
    ></v-text-field>

    <v-card v-for="item in notes" :style="{'margin': '5px'}">
      <v-card-text>
        <div>{{item.user.username}}</div>
        <div><span class="font-weight-bold">{{ item.created_at }}</span> {{ item.text }}</div>
      </v-card-text>
      <v-img v-if="item.image" :src="item.image"></v-img>
    </v-card>
  </v-container>
</template>

<script>
  import header from "../../mixins/header";
  import NoteCreate from "./NoteCreate";

  export default {
    name: 'Note',
    mixins: [header],
    components: {NoteCreate},

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
            let headers = this.getHeaders();
            this.axios.get(`${this.$apiHost}/api/v1/note/`, {
              headers: headers
            }).then((result) =>{
              console.log(result.data)
              this.notes = result.data;
        }).catch((res) => {
            this.dropSession(res);
        })
      }
    }
  }
</script>
