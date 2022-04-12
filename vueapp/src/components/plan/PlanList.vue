<template>
  <v-container>
    <h1 class="text-center">Планы</h1>
    <v-data-table
      :headers="headers"
      :items="plans"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
    ></v-data-table>
  </v-container>
</template>

<script>
export default {
  name: "PlanList",

  data: function () {
    return {
      loading: false,
      plans: [{
        "id": 10,
        "name": "hello world",
        "user": {
            "id": 1,
            "username": "suph4rd",
            "email": "root@gmail.com",
            "is_superuser": true
        },
        "created_at": "16 октября 2021"
    }],
      headers: [
        {
          text: 'Дата',
          align: 'start',
          sortable: false,
          value: 'created_at',
        },
        {
          text: 'Пользователь',
          align: 'start',
          sortable: false,
          value: 'user.username',
        },
        {
          text: 'Название плана',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        {
          text: '',
          align: 'start',
        },
      ],
    }
  }
}
</script>

<style scoped>

</style>