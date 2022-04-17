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
        <div class="actions-btn">
          <v-btn icon :to="{ name: 'PlanDetail', params: {id: item.id} }">
            <v-icon
            class="mr-2"
            >
              mdi-information
            </v-icon>
          </v-btn>
          <PlanUpdate @onUpdate="getData" :objId="item.id"></PlanUpdate>
          <Delete
              @onDelete="getData"
              :objId="item.id"
              :deletePath="'/api/v1/plan/'"
              :titleDelete="'плана'"
              :messageDelete="'план'" ></Delete>
        </div>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import header from "../../mixins/header";
import listMixin from "../../mixins/listMixin";
import PlanCreate from "./PlanCreate";
import PlanUpdate from "./PlanUpdate";
import Delete from "../common_components/Delete";

export default {
  name: "PlanList",
  components: {PlanUpdate, PlanCreate, Delete},
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

<style scoped>
  .actions-btn {
    display: flex;
    justify-content: end;
  }
</style>