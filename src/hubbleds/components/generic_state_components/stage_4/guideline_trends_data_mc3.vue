<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    title-text="Trends in the Data"
    @back="() => {
      state.marker = 'tre_dat2';
      state.define_trend = false;
    }"
    @next="() => {
      state.marker = 'rel_vel1';
      state.define_trend = false;
    }"
    :can-advance="(state) => state.trend_response"
    :state="state"
  >
    <template #before-next>
      Choose a response.
    </template>

    <div>
      <p>
        Now with a larger data set, do you see a trend? Is there a relationship between the velocity and distance of the galaxies?
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="[
            'Yes, I see a trend.',
            'No, I don\'t see a trend.',
            'I can\'t tell if there\'s a trend.',
          ]"
          :feedbacks="[
            'Isn\'t it interesting how adding more data can make a trend more clear?',
            'Try talking to a neighbor or your instructor. Even with a noisy dataset, you should be able to make out some sort of trend',
            'Try talking to a neighbor or your instructor. Even with a noisy dataset, you should be able to make out some sort of trend',
          ]"
          :correct-answers="[]"
          :neutral-answers='[0,1,2]'
          @select="(state) => { this.$emit('ready'); }"
          score-tag="tre-dat-mc3"
        >
        </mc-radiogroup>
        <v-btn
          block
          color="deep-orange darken-2"
          @click="
            state.define_trend = !state.define_trend
          "
        >
          What is a trend?
        </v-btn>
        <v-alert
          class="mt-4 trend-alert" 
          v-if="state.define_trend"
          dense
          color="info darken-1"
        >
          A trend is a pattern in data (for example, an upward <v-icon>mdi-arrow-top-right-bottom-left-bold</v-icon> or downward <v-icon>mdi-arrow-top-left-bottom-right-bold</v-icon> line). 
        </v-alert>
      </v-container>
    </div>
  </scaffold-alert>
</template>


<script>
module.exports = {
  props: ['state']
}
</script>
