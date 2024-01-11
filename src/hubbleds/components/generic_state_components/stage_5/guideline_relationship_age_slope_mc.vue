<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    title-text="Relationship Between Age and Slope"
    @back="state.marker_backward = 1"
    @next="state.marker_forward = 1"
    :can-advance="(state) => state.relage_response"
    :state="state"
  >
    <template #before-next>
      Choose a response.
    </template>
    
    <div
      class="mb-4"
    >
      <p>
        After scanning through your classmates' Hubble graphs, how would you describe the relationship between the slope of the best-fit line and the age of the universe estimated from that dataset?
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <p>The relationship is:</p>
        <mc-radiogroup
          :radio-options="[
            'The data sets that have a steeper slope give a lower estimate for the age of the universe.',
            'The data sets that have a steeper slope give a higher estimate for the age of the universe.',
            'There is no relationship between the slope in a data set and the estimate for the age of the universe.'
          ]"
          :feedbacks="[
            'Yes. Notice that when you drag the slider toward the left (lower age), the slope of the graphed data gets larger (steeper).',
            'Try again. When you drag the slider toward the left (lower age), does the slope of the graphed data get steeper or shallower?',
            'Try again. Drag the slider slowly toward the left (lower age) and observe what happens to the slope of the graphed data. Then drag the slider to the right (higher age) and observe what happens to the slope.'
          ]"
          :correct-answers="[0]"
          @select="onSelect"
          score-tag="age-slope-trend"
        >
        </mc-radiogroup>
      </v-container>
    </div>

  </scaffold-alert>
</template>

<script>
module.exports = {
  props: ['state'],
  methods: {
    onSelect(state) { if (state.correct) { this.$emit('ready'); } }
  }
}
</script>
