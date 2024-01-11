<template>
  <scaffold-alert
    title-text="Measurement Comparison"
    @back="state.marker_backward = 1"
    @next="state.marker_forward = 1"
    :can-advance="(state) => state.dot_seq4a_q"
    :state="state"
  >
    <template #before-next>
        Choose a response
      </template>
    <div
      class="mb-4"
    >
      <p>
        It might be helpful to explore how the angular size and distance measurements relate to each other. Click on different locations in the graph of angular sizes to see what values they correspond to in the distance dot plot above. 
      </p>
      <p>
        What relationship do you see between the angular size and distance measurements?
      </p>
      <mc-radiogroup 
          :radio-options="[
            'A large angular size corresponds to a small distance',
            'A large angular size corresponds to a large distance',
            'There is no relation between distance and the measured angular size',
            ]"
            :feedbacks="[
            'Correct! If two objects have the same size, the one at a larger distance will have a smaller angular size.',
            'Not quite. Look again at the graphs and check two different distance values. Which one has the larger angular size?',
            'Not quite. Look again at the graphs and check two different distance values. Which one has the larger angular size?',
            ]" 
          :correct-answers="[0]"
          :wrong-answers="[1,2]"
          @select="onSelect"
          score-tag="ang_meas_dist_relation">

          </mc-radiogroup>
    </div>
  </scaffold-alert>
</template>


<script>
module.exports = {
 props: ['state'],
  methods: {
   onSelect(opt) { if (opt.correct) { console.log('correct'); this.$emit('ready'); } }
  }
}
</script>
