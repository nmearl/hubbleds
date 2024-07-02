<template>
  <v-card color="info"
          :style="highlighted ? 'border-width: 4px' : ''"
          rounded="5"
          :outlined="highlighted"
  >
    <v-toolbar
            color="primary"
            dense
            dark
            rounded
            flat
        >
          <v-toolbar-title
              class="text-h6 text-uppercase font-weight-regular"
          >
             {{ title }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="calculate_velocity" v-if="show_velocity_button">
            <v-icon>mdi-run-fast</v-icon>
          </v-btn>
        </v-toolbar>

    <v-data-table
        :headers="headers"
        :items="indexedItems"
        :items-per-page="5"
        item-key="id"
        class="elevation-0"
        hide-default-header
        hide-default-footer
        single-select
        :show-select="show_select"
        @item-selected="on_row_selected"
        v-model="selected"
        style="border-radius: 0 !important;"
    >
      <template
          v-slot:header="{ props: { headers } }"
      >
        <thead>
        <tr>
          <th v-for="header in headers">
            <span v-html="header.text"></span>
          </th>
        </tr>
        </thead>
      </template>

      <template v-slot:item.name="{ item }">
        {{ item.galaxy.name }}
      </template>

      <template v-slot:item.element="{ item }">
        {{ item.galaxy.element }}
      </template>

      <template v-slot:item.rest_wave="{ item }">
        {{ item.rest_wave_value }}
      </template>

      <template v-slot:item.obs_wave="{ item }">
        <v-icon v-if="item.obs_wave_value < 1.0">mdi-alert</v-icon>
        <span v-else>{{ item.obs_wave_value }}</span>
      </template>

      <template v-slot:item.velocity="{ item }">
        <v-icon v-if="item.velocity_value < 1.0">mdi-alert</v-icon>
        <span v-else>{{ item.velocity_value }}</span>
      </template>

    </v-data-table>
  </v-card>
</template>

<style scoped>

</style>
<script setup>
module.exports = {
  computed: {
    indexedItems () {
      return this.items.map((item, index) => ({
        id: item.galaxy.name,
        ...item
      }))
    }
  }
}
</script>