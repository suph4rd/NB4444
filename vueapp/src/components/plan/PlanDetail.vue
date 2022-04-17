<template>
  <div>
    <v-container v-if="objects">
      <h1 class="text-center">План {{objects.name}} ({{objects.user.username}})</h1>
      <TaskCreate @onCreate="getData" :plan="objects"></TaskCreate>
      <v-data-table
        :headers="headers"
        :items="objects.task_set"
        :items-per-page="10"
        class="elevation-1"
        :loading="loading"
      >
        <template v-slot:item.is_ready="{ item }">
          <v-simple-checkbox
            v-model="item.is_ready"
            disabled
          ></v-simple-checkbox>
        </template>

        <template v-slot:item.actions="{ item }">
          <div class="actions-btn">
            <TaskUpdate @onUpdate="getData" :objId="item.id"></TaskUpdate>
            <Delete
                @onDelete="getData"
                :objId="item.id"
                :deletePath="'/api/v1/task/'"
                :titleDelete="'задачи'"
                :messageDelete="'задачу'" ></Delete>
          </div>
        </template>
      </v-data-table>
    </v-container>
  </div>
</template>

<script>
import header from "../../mixins/header";
import listMixin from "../../mixins/listMixin";
import TaskCreate from "../task/TaskCreate";
import TaskUpdate from "../task/TaskUpdate";
import Delete from "../common_components/Delete";

export default {
  name: "PlanDetail",
  components: {TaskUpdate, TaskCreate, Delete},
  mixins: [header, listMixin],

  data: function () {
    return {
      loading: false,
      plan: null,
      apiPath: `/api/v1/plan/${this.$route.params.id}`,
      objects: null,
      headers: [
        {
          text: 'Готово',
          align: 'start',
          sortable: false,
          value: 'is_ready',
        },
        {
          text: 'Дата',
          align: 'start',
          sortable: false,
          value: 'created_at',
        },
        {
          text: 'Раздел',
          align: 'start',
          sortable: false,
          value: 'section.name',
        },
        {
          text: 'Описание',
          align: 'start',
          sortable: false,
          value: 'description',
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

</style>