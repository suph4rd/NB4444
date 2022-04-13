<template>
  <v-container>
    <h1 class="text-center">Заметки</h1>
    <NoteCreate :style="{'margin-bottom': '70px'}" @onCreate="getData" />
    <v-text-field
      v-if="!objects"
      color="success"
      loading
      disabled
    ></v-text-field>

    <v-card v-for="item in objects" :style="{'margin': '5px'}">
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
  import listMixin from "../../mixins/listMixin";

  export default {
    name: 'Note',
    mixins: [header, listMixin],
    components: {NoteCreate},

    data: function () {
      return {
        objects: null,
        apiPath: "/api/v1/note/",
      }
    },
  }
</script>
