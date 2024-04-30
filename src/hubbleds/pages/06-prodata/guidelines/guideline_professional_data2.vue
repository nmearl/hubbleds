<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="question_completed && can_advance"
    
  >
    <div
      class="mb-4"
    >
    <p>Is your age estimate higher than or lower than Hubble's age estimate?</p>
      <v-container
        class="px-0"
        fluid
      >
        <mc-radiogroup
          :radio-options="[
            'Our class got a higher age estimate than Hubble',
            'Our class got a lower age estimate than Hubble.'
          ]"
          :feedbacks="[
            'Correct! Because the slope of the trend in our data is shallower than the trend in Hubble\'s data, our age estimate must be higher ',
            'Remember, the slope of the trend in our data is shallower than the trend in Hubble\'s data, so our age estimate must be higher.'
          ]"
          :correct-answers="[0]"
          @select="(status) => { if (status.correct) { question_completed = true; } }"
          :score-tag="state_view.score_tag"
          @mc-initialize-response="mc_callback(['mc-initialize-response',$event])"
          @mc-score="mc_callback(['mc-score',$event])"
          :initialization="state_view.mc_score"
        >
        </mc-radiogroup>
      </v-container>
    </div>
  </scaffold-alert>
</template>

<script>
module.exports = {
  data() {
    return {
      question_completed: false,
    };
  },
};
</script>



