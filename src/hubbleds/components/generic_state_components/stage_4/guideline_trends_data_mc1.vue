<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    title-text="Trends in the Data"
    @back="() => {
      state.marker = 'exp_dat1';
      state.define_trend = false;
    }"
    @next="() => {
        state.marker = 'tre_dat2';
        state.define_trend = false;
        state.trend_response = false;
      }
    "
    :can-advance="(state) => state.trend_response"
    :state="state"
  >
    <template #before-next>
      Choose a response.
    </template>

    <div>
      <p>
        The graph here shows the velocities of your galaxies plotted vs. their distances.  
      </p>
      <p>
        Do you see any sort of trend in your data? Is there a relationship between the velocities and distances of the galaxies?
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
            'Interesting, but it might help to look at more data before deciding for sure.',
            'Yeah, it can be hard with so few data points. Let\'s see what happens if we add more data.',
            'Yeah, it can be hard with so few data points. Let\'s see what happens if we add more data.',
          ]"
          :correct-answers="[]"
          :neutral-answers='[0,1,2]'
          @select="(state) => { this.$emit('ready'); }"
          score-tag="tre-dat-mc1"
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
          A trend is a pattern in data (for example, an upward line <v-icon>mdi-arrow-top-right-bottom-left-bold</v-icon> or downward line <v-icon>mdi-arrow-top-left-bottom-right-bold</v-icon>). 
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
