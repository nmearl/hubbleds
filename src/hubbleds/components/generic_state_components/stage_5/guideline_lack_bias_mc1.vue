<!-- this state.marker = 'lac_bia1' -->
<template>
  <scaffold-alert
    title-text="Which Might Produce a Closer Result?"
    @back="state.marker_backward = 1"
    @next="state.marker_forward = 1"
    :can-advance="(state) => state.lack_bias_response"
    :state="state"
  >
    <div
      class="mb-4"
    >
      <p>
        Let’s assume for a moment that there is no systematic uncertainty (or bias) in our measurements. That would mean that the true value for the age of the universe should lie within the range of measured values, most likely at the middle.
      </p>
      <p>
        Now let's imagine randomly selecting one student's measured age value from all the student measurements and one class's measured age value from all the class measurements.
      </p>
      <v-container
        class="px-0"
        fluid
      >
        <p>Which randomly chosen age measurement&#8212;the student's or the class's&#8212;is likely to be closer to the true age of the universe?</p>
        <mc-radiogroup
          :radio-options="[
            'The age measured by the randomly chosen class is more likely to be closer to the true age of the universe.',
            'The age measured by the randomly chosen student is more likely to be closer to the true age of the universe.',
            'The ages measured by the randomly chosen class and the randomly chosen student have the same likelihood of being closer to the true age of the universe.'
          ]"
          :feedbacks="[
            'That’s right. The age measured by the randomly chosen class is more likely to be closer to the true age of the universe. Let’s explore why.',
            'Not quite. Think about the range of ages spanned by each histogram. If a measurement is randomly chosen from each histogram, which is likely to be closer to the middle of the range? Try again.',
            'Not quite. Think about the range of ages spanned by each histogram. If a measurement is randomly chosen from each histogram, which is likely to be closer to the middle of the range? Try again.',
          ]"
          :correct-answers="[0]"
          :wrong-answers='[1,2]'
          @select="onSelect"
          score-tag="closer-results"
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
