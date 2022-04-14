<template>
  <v-container>
    <h1 class="text-center">Планы</h1>
    <PlanCreate @onCreate="getData"></PlanCreate>
    <v-data-table
      :headers="headers"
      :items="objects"
      :items-per-page="10"
      class="elevation-1"
      :loading="loading"
    >
      <template v-slot:item.actions="{ item }">
        <v-btn icon :to="{ name: 'PlanDetail', params: {id: item.id} }">
          Просмотр
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import header from "../../mixins/header";
import listMixin from "../../mixins/listMixin";
import PlanCreate from "./PlanCreate";

export default {
  name: "PlanList",
  components: {PlanCreate},
  mixins: [header, listMixin],

  data: function () {
    return {
      loading: false,
      apiPath: "/api/v1/plan/",
      objects: [],
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
          value: 'actions',
        },
      ],
    }
  },
}
</script>